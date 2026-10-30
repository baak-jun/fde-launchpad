"""Run tests and synthetic baselines; persist evidence with code hashes."""
import asyncio
import hashlib
import json
import os
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))

if __name__=='__main__':
    out=ROOT/'evidence/runtime'
    out.mkdir(parents=True,exist_ok=True)
    environment={**os.environ,'PYTHONIOENCODING':'utf-8','PYDANTIC_AI_NO_BANNER':'1'}
    test=subprocess.run([sys.executable,'-m','unittest','discover','-s','tests','-v'],cwd=ROOT,env=environment,capture_output=True,encoding='utf-8')
    (out/'tests.log').write_text(test.stdout+test.stderr,encoding='utf-8')
    from runtime.capabilities import run
    from runtime.domains import load_domains
    from runtime.providers import RuleProvider,generate
    capabilities={name:run(name) for name in ['documents','analytics','planner','recommendation']}
    (out/'capabilities.json').write_text(json.dumps(capabilities,ensure_ascii=False,indent=2),encoding='utf-8')
    fixture=json.loads((ROOT/'examples/support-triage.json').read_text(encoding='utf-8'))
    cases=[]
    for case in fixture['cases']:
        result=asyncio.run(generate(load_domains()['support'],case['input'],RuleProvider()))
        observed=result['proposal']['category']
        cases.append({'id':case['id'],'expected_category':case['expected_category'],'observed_category':observed,
                      'category_match':observed==case['expected_category'],'blocked':bool(result['proposal']['blocked_reason'])})
    evaluation={'mode':'rules_baseline_not_llm','dataset':'synthetic support-triage, 12 cases',
                'scope':'Category agreement only; fixture expected_action is NOT fully implemented or scored.',
                'matched':sum(c['category_match'] for c in cases),'total':len(cases),'cases':cases}
    (out/'baseline-evaluation.json').write_text(json.dumps(evaluation,ensure_ascii=False,indent=2),encoding='utf-8')
    sources=[ROOT/'kit.py',ROOT/'run_workbench.py',ROOT/'requirements.lock']
    for folder in ['runtime','domain_packs','tests','scripts','examples','catalog','templates','skills']:
        sources += [p for p in (ROOT/folder).rglob('*') if p.is_file() and '__pycache__' not in p.parts]
    report={'checked_at_utc':datetime.now(timezone.utc).isoformat(),'test_exit_code':test.returncode,
            'code_hashes':{p.relative_to(ROOT).as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for p in sources},
            'live_llm_tested':False,'remote_connector_tested':False,'native_mobile_tested':False}
    (out/'verification.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps({'tests_passed':test.returncode==0,'baseline_category_matches':evaluation['matched'],'baseline_cases':len(cases),'evidence':str(out)},ensure_ascii=False))
    raise SystemExit(test.returncode)
