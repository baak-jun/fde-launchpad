"""Read-only local environment check. Never print credentials."""
import importlib.metadata
import json
import platform
import sqlite3
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]

if __name__=='__main__':
    packages={}
    for name in ['fastapi','uvicorn','pydantic-ai-slim','httpx','duckdb','ortools','markitdown']:
        try:
            packages[name]=importlib.metadata.version(name)
        except importlib.metadata.PackageNotFoundError:
            packages[name]=None
    print(json.dumps({'python':platform.python_version(),'os':platform.system(),'architecture':platform.machine(),
                      'sqlite':sqlite3.sqlite_version,'packages':packages,'domains':len(list((ROOT/'domain_packs').glob('*.json'))),
                      'missing_packages':[k for k,v in packages.items() if v is None]},ensure_ascii=False,indent=2))
    raise SystemExit(1 if any(v is None for v in packages.values()) else 0)
