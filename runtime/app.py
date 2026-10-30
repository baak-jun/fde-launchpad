import os
import secrets
from pathlib import Path
from fastapi import Depends, FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from starlette.middleware.trustedhost import TrustedHostMiddleware
from .domains import ROOT, load_domains
from .providers import RuleProvider, PydanticProvider, generate
from .schemas import Principal, Submit, Revision, Decision, Execution
from .store import Store, StoreError


def create_app(db_path=None, provider=None, identities=None, daily_limit=100):
    app = FastAPI(title='FDE Workbench', version='0.1.0', docs_url='/api/docs', openapi_url='/api/openapi.json')
    app.add_middleware(TrustedHostMiddleware, allowed_hosts=['127.0.0.1', 'localhost', 'testserver'])
    store = Store(db_path or ROOT / 'runtime-data/workbench.sqlite3')
    domains = load_domains()
    provider = provider or RuleProvider()
    # Local bootstrap is intentionally NOT a production identity provider.
    # When identities are injected, public HTML does not expose any of their keys.
    browser_token = secrets.token_urlsafe(32) if identities is None else ''
    identities = identities if identities is not None else {browser_token: Principal(tenant='local-demo', actor='local-operator')}
    app.state.store, app.state.provider = store, provider

    @app.exception_handler(StoreError)
    async def store_error(request, exc):
        return JSONResponse({'detail': exc.message}, status_code=exc.status)

    @app.middleware('http')
    async def boundary(request, call_next):
        origin = request.headers.get('origin')
        if origin and origin != str(request.base_url).rstrip('/'):
            return JSONResponse({'detail': 'Cross-origin request denied'}, status_code=403)
        length = request.headers.get('content-length')
        if length and (not length.isdigit() or int(length) > 40000):
            return JSONResponse({'detail': 'Request body too large'}, status_code=413)
        # Count actual streamed bytes, including chunked requests, before parsing JSON.
        if request.method in {'POST', 'PATCH', 'PUT'}:
            chunks, size = [], 0
            async for chunk in request.stream():
                size += len(chunk)
                if size > 40000:
                    return JSONResponse({'detail': 'Request body too large'}, status_code=413)
                chunks.append(chunk)
            request._body = b''.join(chunks)
        response = await call_next(request)
        response.headers['Cache-Control'] = 'no-store'
        response.headers['X-Content-Type-Options'] = 'nosniff'
        response.headers['Content-Security-Policy'] = "default-src 'self'; script-src 'self'; style-src 'self'; img-src 'self' data:; frame-ancestors 'none'; base-uri 'none'; form-action 'self'"
        return response

    def principal(request: Request):
        value = request.headers.get('authorization', '')
        token = value.removeprefix('Bearer ') if value.startswith('Bearer ') else ''
        identity = identities.get(token)
        if identity is None:
            raise HTTPException(401, '인증 정보가 필요합니다.')
        return identity

    def require(identity, role):
        if role not in identity.roles:
            raise HTTPException(403, '이 작업의 권한이 없습니다.')

    def pack(domain):
        if domain not in domains:
            raise HTTPException(422, '등록되지 않은 도메인입니다.')
        return domains[domain]

    async def process(identity, domain, text):
        selected = pack(domain)
        if not text.strip():
            raise HTTPException(422, '요청 내용을 입력하세요.')
        if provider.mode == 'live_model':
            store.reserve_calls(identity, daily_limit)
        return await generate(selected, text, provider)

    @app.get('/', response_class=HTMLResponse)
    def home():
        html = (ROOT / 'runtime/web/index.html').read_text(encoding='utf-8')
        return html.replace('__BOOTSTRAP_TOKEN__', browser_token)

    @app.get('/api/health')
    def health():
        return {'status': 'ok', 'mode': provider.mode, 'execution': 'local_sandbox_only', 'identity': 'local_operator_demo'}

    @app.get('/api/domains')
    def get_domains(identity=Depends(principal)):
        return list(domains.values())

    @app.get('/api/jobs')
    def jobs(identity=Depends(principal)):
        return store.list(identity)

    @app.get('/api/jobs/{job_id}')
    def get_job(job_id: str, identity=Depends(principal)):
        return store.get(identity, job_id)

    @app.post('/api/jobs', status_code=201)
    async def submit(body: Submit, identity=Depends(principal)):
        require(identity, 'submit')
        existing = store.existing(identity, body)
        if existing:
            return existing
        result = await process(identity, body.domain, body.text)
        return store.create(identity, body, result)

    @app.patch('/api/jobs/{job_id}')
    async def revise(job_id: str, body: Revision, identity=Depends(principal)):
        require(identity, 'submit')
        current = store.get(identity, job_id)
        store.check_version(current, body.expected_version)
        if current['status'] == 'completed':
            raise HTTPException(409, '완료된 요청은 수정할 수 없습니다.')
        result = await process(identity, current['domain'], body.text)
        return store.revise(identity, job_id, body.text, body.expected_version, result)

    @app.post('/api/jobs/{job_id}/decision')
    def decision(job_id: str, body: Decision, identity=Depends(principal)):
        require(identity, 'review')
        return store.decide(identity, job_id, body.decision, body.expected_version)

    @app.post('/api/jobs/{job_id}/execute')
    def execute(job_id: str, body: Execution, identity=Depends(principal)):
        require(identity, 'execute')
        return store.execute(identity, job_id, body.expected_version, body.proposal_hash)

    app.mount('/static', StaticFiles(directory=ROOT / 'runtime/web'), name='static')
    return app


def configured_app():
    live = os.environ.get('FDE_ENABLE_LIVE') == '1'
    model = os.environ.get('FDE_MODEL')
    if live and not model:
        raise RuntimeError('FDE_MODEL must be set when live mode is enabled')
    provider = PydanticProvider(model) if live else RuleProvider()
    return create_app(provider=provider, daily_limit=int(os.environ.get('FDE_DAILY_CALL_LIMIT', '100')))
