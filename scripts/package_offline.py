"""Bundle source and exact Windows/Python wheel dependencies, excluding keys and DBs."""
import hashlib
import json
import re
from datetime import datetime,timezone
from email.parser import BytesParser
from pathlib import Path
from zipfile import ZipFile, ZIP_DEFLATED
from checkpoint import checkpoint

ROOT=Path(__file__).resolve().parents[1]


def normalize(name):
    return re.sub(r'[-_.]+','-',name).lower()


def package():
    required={}
    for line in (ROOT/'requirements.lock').read_text(encoding='utf-8').splitlines():
        if line.strip() and not line.startswith('#'):
            name,version=line.split('==')
            required[normalize(name)]=version
    wheels={}
    for path in (ROOT/'.cache/wheels').glob('*.whl'):
        with ZipFile(path) as wheel:
            name=next(n for n in wheel.namelist() if n.endswith('.dist-info/METADATA'))
            metadata=BytesParser().parsebytes(wheel.read(name))
            key=normalize(metadata['Name'])
            if required.get(key)==metadata['Version']:
                wheels[key]=path
    missing=set(required)-set(wheels)
    if missing:
        raise ValueError('Wheel cache incomplete: '+', '.join(sorted(missing)))
    source=checkpoint('offline-source')
    stamp=datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S%fZ')
    output=ROOT/'backups'/f'{stamp}-fde-offline-windows-py313.zip'
    with ZipFile(source) as original, ZipFile(output,'x',ZIP_DEFLATED) as bundle:
        hashes=json.loads(original.read('CHECKPOINT_MANIFEST.json'))
        for name in hashes:
            bundle.writestr(name,original.read(name))
        for path in sorted(wheels.values()):
            name='.cache/wheels/'+path.name
            data=path.read_bytes()
            hashes[name]=hashlib.sha256(data).hexdigest()
            bundle.writestr(name,data)
        bundle.writestr('CHECKPOINT_MANIFEST.json',json.dumps(hashes,ensure_ascii=False,indent=2))
    with ZipFile(output) as bundle:
        assert bundle.testzip() is None
        for name,digest in hashes.items():
            assert hashlib.sha256(bundle.read(name)).hexdigest()==digest
    report={'path':str(output),'source_archive':str(source),'files':len(hashes),'wheels':len(wheels),
            'bytes':output.stat().st_size,'sha256':hashlib.sha256(output.read_bytes()).hexdigest(),
            'platform':'Windows x64 CPython 3.13','contains_keys':False,'contains_runtime_database':False}
    print(json.dumps(report,ensure_ascii=False))
    (ROOT/'evidence/runtime/offline-bundle.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
    return output


if __name__=='__main__':
    package()
