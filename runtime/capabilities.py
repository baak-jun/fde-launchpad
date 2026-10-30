"""Small reusable adapters; each reports its algorithm and limits explicitly."""
import csv
import io
import json
import re
from pathlib import Path
from .domains import ROOT

SAMPLES = ROOT / 'examples/capabilities'


def documents(query='환불', tenant='alpha', records=None):
    from markitdown import MarkItDown
    records = records if records is not None else json.loads((SAMPLES / 'documents.json').read_text(encoding='utf-8'))
    terms = set(re.findall(r'[\w가-힣]+',query.casefold()))
    if not terms or len(query)>500:
        raise ValueError('Query must contain words and be at most 500 characters')
    converter = MarkItDown(enable_plugins=False)
    matches=[]
    # Authorization filtering happens before conversion/ranking. The tenant argument
    # must come from a trusted identity in a real API, never an end-user query field.
    for record in records:
        if record['tenant'] != tenant:
            continue
        converted=converter.convert_stream(io.BytesIO(record['text'].encode('utf-8')),file_extension='.txt').text_content
        score=sum(term in converted.casefold() for term in terms)
        if score:
            matches.append({'source_id':record['id'],'quote':converted,'score':score})
    matches.sort(key=lambda x:(-x['score'],x['source_id']))
    return {'mode':'markitdown_plus_keyword_baseline','status':'found' if matches else 'abstained','matches':matches[:3],
            'limitation':'Literal text retrieval, not semantic RAG or generated factual answers; sample text only, OCR not tested.'}


def analytics(path=None):
    import duckdb
    path=Path(path) if path else SAMPLES / 'orders.csv'
    if path.stat().st_size>2_000_000:
        raise ValueError('CSV limit: 2 MB')
    with path.open(encoding='utf-8-sig',newline='') as stream:
        reader=csv.DictReader(stream)
        if reader.fieldnames!=['order_id','category','quantity','unit_price_krw']:
            raise ValueError('Unexpected CSV columns')
        rows=[]
        seen=set()
        for row in reader:
            if len(rows)>=10000:
                raise ValueError('CSV row limit exceeded')
            quantity,price=int(row['quantity']),int(row['unit_price_krw'])
            if not 0<quantity<=10000 or not 0<=price<=1_000_000_000 or row['order_id'] in seen:
                raise ValueError('Invalid amount or duplicate order ID')
            seen.add(row['order_id'])
            rows.append((row['order_id'],row['category'],quantity,price))
    if not rows:
        raise ValueError('CSV has no data rows')
    db=duckdb.connect(config={'enable_external_access':'false','threads':'1','memory_limit':'128MB'})
    try:
        db.execute('CREATE TABLE orders(id VARCHAR, category VARCHAR, quantity BIGINT, price BIGINT)')
        db.executemany('INSERT INTO orders VALUES(?,?,?,?)',rows)
        totals=db.execute('SELECT category, SUM(quantity*price) AS revenue FROM orders GROUP BY category ORDER BY category').fetchall()
        return {'mode':'duckdb_fixed_query','currency':'KRW','totals':[{'category':c,'revenue':int(n)} for c,n in totals],
                'grand_total':sum(int(n) for _,n in totals),'row_count':len(rows),
                'limitation':'Only this validated order schema and fixed aggregation; arbitrary SQL is not accepted.'}
    finally:
        db.close()


def planner(spec=None):
    from ortools.sat.python import cp_model
    spec=spec if spec is not None else json.loads((SAMPLES / 'schedule.json').read_text(encoding='utf-8'))
    slots,people=spec['slots'],spec['people']
    if not 1<=len(slots)<=40 or not 1<=len(people)<=40 or len(set(slots))!=len(slots) or len({p['id'] for p in people})!=len(people):
        raise ValueError('Use 1-40 unique slots and people')
    if any(not set(p['allowed'])<=set(slots) for p in people):
        raise ValueError('Unknown allowed slot')
    model=cp_model.CpModel()
    choices={}
    for person in people:
        variables=[]
        for slot in person['allowed']:
            key=(person['id'],slot)
            if key in choices:
                raise ValueError('Repeated allowed slot')
            choices[key]=model.new_bool_var(person['id']+'_'+slot)
            variables.append(choices[key])
        model.add(sum(variables)==1)
    for slot in slots:
        model.add(sum(v for (person,s),v in choices.items() if s==slot)<=1)
    model.maximize(sum(v for (person,slot),v in choices.items() if any(p['id']==person and p.get('preferred')==slot for p in people)))
    solver=cp_model.CpSolver()
    solver.parameters.max_time_in_seconds=2
    solver.parameters.num_search_workers=1
    status=solver.solve(model)
    result={'mode':'ortools_cp_sat','status':solver.status_name(status),'assignments':[], 'preferred_count':None,
            'limitation':'One person per slot; not a live booking system or concurrent reservation service.'}
    if status in (cp_model.OPTIMAL,cp_model.FEASIBLE):
        result['assignments']=[{'person':p,'slot':s} for (p,s),v in choices.items() if solver.value(v)]
        result['preferred_count']=int(solver.objective_value)
    return result


def recommendation(interests=None, items=None, excluded=None):
    items=items if items is not None else json.loads((SAMPLES / 'items.json').read_text(encoding='utf-8'))
    interests=set(interests or [])
    excluded=set(excluded or [])
    eligible=[i for i in items if i['available'] and i['id'] not in excluded]
    ranked=sorted(eligible,key=lambda i:(-len(interests.intersection(i['tags'])),-i['popularity'],i['id']))
    return {'mode':'transparent_rules_baseline','cold_start':not interests,
            'items':[{'id':i['id'],'title':i['title'],'matched_tags':sorted(interests.intersection(i['tags'])),'popularity':i['popularity']} for i in ranked[:3]],
            'limitation':'No trained recommender. This is a cold-start baseline for comparison with implicit once real interaction data exists.'}


def run(name):
    if name=='documents':
        return documents()
    if name=='analytics':
        return analytics()
    if name=='planner':
        return planner()
    if name=='recommendation':
        return recommendation(['python','data'])
    raise ValueError('Unknown capability')
