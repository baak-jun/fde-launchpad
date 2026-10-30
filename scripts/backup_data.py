"""SQLite online backup of local workbench state, separate from source ZIPs."""
import hashlib
import json
import sys
from datetime import datetime,timezone
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from runtime.store import Store

if __name__=='__main__':
    source=ROOT/'runtime-data/workbench.sqlite3'
    if not source.exists():
        raise SystemExit('No runtime database exists yet.')
    destination=ROOT/'backups'/('data-'+datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S%fZ')+'.sqlite3')
    Store(source).backup(destination)
    print(json.dumps({'path':str(destination),'sha256':hashlib.sha256(destination.read_bytes()).hexdigest(),'integrity':'ok'},ensure_ascii=False))
