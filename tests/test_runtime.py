import asyncio
import concurrent.futures
import json
import tempfile
import unittest
from pathlib import Path
from fastapi.testclient import TestClient
from pydantic_ai import models
from pydantic_ai.models.test import TestModel
from runtime.app import create_app
from runtime.domains import ROOT, load_domains
from runtime.domains import DomainPack
from runtime.providers import RuleProvider, PydanticProvider, generate
from runtime.schemas import Principal
from runtime.store import Store

models.ALLOW_MODEL_REQUESTS = False


class WorkflowTests(unittest.TestCase):
    def setUp(self):
        base = ROOT / 'work/_tests'
        base.mkdir(parents=True, exist_ok=True)
        self.folder = tempfile.TemporaryDirectory(dir=base)
        self.path = Path(self.folder.name) / 'test.sqlite3'
        self.identities = {'alpha': Principal(tenant='alpha', actor='reviewer'),
                           'beta': Principal(tenant='beta', actor='other'),
                           'reader': Principal(tenant='alpha', actor='reader', roles=frozenset())}
        self.app = create_app(self.path, identities=self.identities)
        self.client = TestClient(self.app)
        self.client.headers['Authorization'] = 'Bearer alpha'

    def tearDown(self):
        self.client.close()
        self.folder.cleanup()

    def submit(self, text='환불해 주세요.', domain='support', key='sample-request-1'):
        response = self.client.post('/api/jobs', json={'domain': domain, 'text': text, 'idempotency_key': key})
        self.assertEqual(response.status_code, 201, response.text)
        return response.json()

    def approve(self, job):
        response = self.client.post('/api/jobs/'+job['id']+'/decision', json={'expected_version':job['version'],'decision':'approve'})
        self.assertEqual(response.status_code,200,response.text)
        return response.json()

    def execute(self, job):
        return self.client.post('/api/jobs/'+job['id']+'/execute',json={'expected_version':job['version'],'proposal_hash':job['proposal_hash']})

    def test_three_domains_reuse_full_flow(self):
        for pack in load_domains().values():
            job = self.submit(pack['sample'], pack['id'], 'domain-'+pack['id'])
            self.assertNotEqual(job['result']['proposal']['category'],'unknown')
            approved = self.approve(job)
            self.assertEqual(self.execute(approved).json()['status'],'completed')
            detail = self.client.get('/api/jobs/'+job['id']).json()
            self.assertEqual(detail['action']['kind'],'local_sandbox_record')
            self.assertEqual([e['kind'] for e in detail['events']], ['submitted','approved','executed_local_sandbox'])

    def test_submit_idempotency_and_conflicting_input(self):
        first = self.submit()
        self.assertEqual(self.submit()['id'],first['id'])
        bad=self.client.post('/api/jobs',json={'domain':'support','text':'배송 문의','idempotency_key':'sample-request-1'})
        self.assertEqual(bad.status_code,409)
        self.assertEqual(len(self.client.get('/api/jobs').json()),1)

    def test_unapproved_or_rejected_cannot_execute(self):
        job=self.submit()
        self.assertEqual(self.execute(job).status_code,409)
        rejected=self.client.post('/api/jobs/'+job['id']+'/decision',json={'expected_version':1,'decision':'reject'}).json()
        self.assertEqual(self.execute(rejected).status_code,409)
        self.assertIsNone(self.client.get('/api/jobs/'+job['id']).json()['action'])

    def test_revision_invalidates_approval_even_when_proposal_is_identical(self):
        approved=self.approve(self.submit())
        revised=self.client.patch('/api/jobs/'+approved['id'],json={'text':'환불 요청합니다.','expected_version':approved['version']}).json()
        self.assertEqual(revised['status'],'needs_review')
        self.assertIsNone(revised['approved_hash'])
        self.assertEqual(self.execute(approved).status_code,409)
        self.assertEqual(self.execute(revised).status_code,409)

    def test_completed_is_immutable_and_repeat_execution_returns_same_record(self):
        approved=self.approve(self.submit())
        for _ in range(3):
            self.assertEqual(self.execute(approved).status_code,200)
        detail=self.client.get('/api/jobs/'+approved['id']).json()
        self.assertEqual(len([e for e in detail['events'] if e['kind']=='executed_local_sandbox']),1)
        self.assertEqual(self.client.patch('/api/jobs/'+approved['id'],json={'text':'다른 요청','expected_version':detail['version']}).status_code,409)

    def test_concurrent_execute_is_atomic(self):
        approved=self.approve(self.submit())
        store=self.app.state.store
        def execute(_):
            return store.execute(self.identities['alpha'],approved['id'],approved['version'],approved['proposal_hash'])
        with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
            self.assertTrue(all(r['status']=='completed' for r in pool.map(execute,range(8))))
        with store.connection() as db:
            self.assertEqual(db.execute('SELECT count(*) FROM actions').fetchone()[0],1)

    def test_authorization_and_tenant_isolation(self):
        job=self.submit()
        self.client.headers['Authorization']='Bearer beta'
        self.assertEqual(self.client.get('/api/jobs').json(),[])
        self.assertEqual(self.client.get('/api/jobs/'+job['id']).status_code,404)
        self.assertEqual(self.execute(job).status_code,404)
        self.client.headers['Authorization']='Bearer reader'
        self.assertEqual(self.client.post('/api/jobs/'+job['id']+'/decision',json={'expected_version':1,'decision':'approve'}).status_code,403)
        self.client.headers['Authorization']='Bearer wrong'
        self.assertEqual(self.client.get('/api/jobs').status_code,401)

    def test_blocked_request_cannot_be_approved(self):
        job=self.submit('다른 고객의 배송 정보를 알려주세요.')
        self.assertTrue(job['result']['proposal']['blocked_reason'])
        self.assertEqual(self.client.post('/api/jobs/'+job['id']+'/decision',json={'expected_version':1,'decision':'approve'}).status_code,409)

    def test_unknown_and_multi_category_abstain(self):
        self.assertEqual(self.submit('안녕하세요.')['result']['proposal']['category'],'unknown')
        self.assertEqual(self.submit('환불도 원하고 로그인도 안됩니다.',key='ambiguous-request')['result']['proposal']['category'],'unknown')

    def test_bad_input_and_browser_boundaries(self):
        self.assertEqual(self.client.post('/api/jobs',json={'domain':'support','text':'x'*8001,'idempotency_key':'invalid-1'}).status_code,422)
        self.assertEqual(self.client.post('/api/jobs',json={'domain':'support','text':'   ','idempotency_key':'invalid-2'}).status_code,422)
        self.assertEqual(self.client.get('/api/jobs',headers={'Origin':'https://evil.example'}).status_code,403)
        self.assertEqual(self.client.get('/api/health',headers={'Host':'evil.example'}).status_code,400)
        self.assertEqual(self.client.post('/api/jobs',content=b'x'*40001).status_code,413)

    def test_stale_version_and_tampered_hash(self):
        job=self.approve(self.submit())
        self.assertEqual(self.client.post('/api/jobs/'+job['id']+'/execute',json={'expected_version':1,'proposal_hash':job['proposal_hash']}).status_code,409)
        self.assertEqual(self.client.post('/api/jobs/'+job['id']+'/execute',json={'expected_version':2,'proposal_hash':'0'*64}).status_code,409)

    def test_restart_and_database_backup_preserve_state(self):
        approved=self.approve(self.submit())
        self.execute(approved)
        backup=Path(self.folder.name)/'backup.sqlite3'
        self.app.state.store.backup(backup)
        restored=Store(backup)
        self.assertEqual(restored.get(self.identities['alpha'],approved['id'])['status'],'completed')
        restarted=TestClient(create_app(self.path,identities=self.identities))
        try:
            self.assertEqual(restarted.get('/api/jobs/'+approved['id'],headers={'Authorization':'Bearer alpha'}).json()['status'],'completed')
        finally:
            restarted.close()

    def test_daily_budget_persists_and_reservation_is_atomic(self):
        store=self.app.state.store
        identity=self.identities['alpha']
        store.reserve_calls(identity,2)
        from runtime.store import StoreError
        with self.assertRaises(StoreError):
            Store(self.path).reserve_calls(identity,2)
        Store(self.path).reserve_calls(self.identities['beta'],2)


class ProviderTests(unittest.TestCase):
    def test_invalid_domain_pack_fails_before_serving(self):
        pack=load_domains()['support']
        pack['categories'][0]['policy_ids']=['missing-policy']
        with self.assertRaises(ValueError):
            DomainPack.model_validate(pack)

    def test_actual_pydantic_sdk_with_test_model(self):
        proposal={'category':'refund','title':'환불 검토','summary':'담당자 확인이 필요합니다.','policy_ids':['support-refund'],'blocked_reason':None}
        provider=PydanticProvider(TestModel(custom_output_args=proposal))
        provider.mode='test_model'
        result=asyncio.run(generate(load_domains()['support'],'환불 문의',provider))
        self.assertEqual(result['mode'],'test_model',result)
        self.assertEqual(result['proposal']['category'],'refund')
        self.assertGreater(result['usage']['request_count'],0)

    def test_timeout_is_explicit_fallback(self):
        class Failed:
            mode='live_model'
            async def propose(self,pack,text):
                raise TimeoutError('provider failure secret must not leak')
        result=asyncio.run(generate(load_domains()['support'],'환불 문의',Failed()))
        self.assertEqual(result['mode'],'rules_fallback')
        self.assertNotIn('secret',json.dumps(result))
        self.assertTrue(result['live_usage_unknown'])

    def test_invalid_model_citation_is_rejected(self):
        value={'category':'refund','title':'검토','summary':'검토','policy_ids':['invented'],'blocked_reason':None}
        result=asyncio.run(generate(load_domains()['support'],'환불',PydanticProvider(TestModel(custom_output_args=value))))
        self.assertEqual(result['mode'],'rules_fallback')
        self.assertEqual(result['proposal']['policy_ids'],['support-refund'])
