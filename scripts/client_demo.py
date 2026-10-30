"""Exercise the same loopback HTTP API from a CLI. No external system writes."""
import argparse
import json
import re
import urllib.parse
import urllib.request
import uuid
from pathlib import Path

if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--url',default='http://127.0.0.1:8765')
    parser.add_argument('--domain',default='support')
    parser.add_argument('--execute',action='store_true',help='Approve and create one local sandbox record')
    parser.add_argument('--output')
    args=parser.parse_args()
    target=urllib.parse.urlsplit(args.url)
    if target.scheme!='http' or target.hostname not in {'127.0.0.1','localhost'} or target.username or target.password or target.path not in {'','/'} or target.query or target.fragment:
        raise SystemExit('Only a loopback workbench base URL is accepted')
    base=args.url.rstrip('/')
    opener=urllib.request.build_opener(urllib.request.ProxyHandler({}))
    with opener.open(base+'/',timeout=10) as response:
        html=response.read().decode('utf-8')
    match=re.search(r'name="fde-token" content="([A-Za-z0-9_-]+)"',html)
    if not match:
        raise SystemExit('Local demo bootstrap is unavailable; do not use this CLI as a production login client')
    token=match.group(1)
    def call(path,body=None):
        req=urllib.request.Request(base+'/api'+path,data=json.dumps(body).encode() if body is not None else None,
            headers={'Authorization':'Bearer '+token,'Content-Type':'application/json'})
        with opener.open(req,timeout=40) as response:
            return json.load(response)
    pack=next((d for d in call('/domains') if d['id']==args.domain),None)
    if pack is None:
        raise SystemExit('Unknown domain')
    job=call('/jobs',{'domain':pack['id'],'text':pack['sample'],'idempotency_key':uuid.uuid4().hex})
    if args.execute:
        job=call('/jobs/'+job['id']+'/decision',{'decision':'approve','expected_version':job['version']})
        job=call('/jobs/'+job['id']+'/execute',{'expected_version':job['version'],'proposal_hash':job['proposal_hash']})
    detail=call('/jobs/'+job['id'])
    report={'domain':pack['id'],'job_id':job['id'],'status':job['status'],'mode':job['result']['mode'],
            'events':[e['kind'] for e in detail['events']], 'local_action_created':bool(detail['action'])}
    if args.output:
        Path(args.output).write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps(report,ensure_ascii=False,indent=2))
