"""Create a source-only ZIP and verify every entry; never overwrite a checkpoint."""
import argparse
import hashlib
import json
import os
from datetime import datetime, timezone
from pathlib import Path
from zipfile import ZipFile, ZIP_DEFLATED

ROOT = Path(__file__).resolve().parents[1]
EXCLUDED = {'.git', 'backups', '__pycache__', '.venv', 'node_modules', 'work', '.cache', 'runtime-data'}

def checkpoint(label):
    if not label or any(c not in 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-_' for c in label):
        raise ValueError('label: letters, digits, - and _ only')
    stamp = datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S%fZ')
    out = ROOT / 'backups' / f'{stamp}-{label}.zip'
    out.parent.mkdir(exist_ok=True)
    hashes = {}
    with ZipFile(out, 'x', ZIP_DEFLATED) as archive:
        for directory, folders, files in os.walk(ROOT, followlinks=False):
            folders[:] = sorted(f for f in folders if f not in EXCLUDED and not (Path(directory)/f).is_symlink() and not getattr(Path(directory)/f, 'is_junction', lambda: False)())
            for filename in sorted(files):
                path = Path(directory)/filename
                relative = path.relative_to(ROOT)
                if path.is_symlink() or not path.resolve().is_relative_to(ROOT.resolve()):
                    continue
                if path.name.startswith('.env') and path.name != '.env.example':
                    continue
                data = path.read_bytes()
                hashes[relative.as_posix()] = hashlib.sha256(data).hexdigest()
                archive.writestr(relative.as_posix(), data)
        archive.writestr('CHECKPOINT_MANIFEST.json', json.dumps(hashes, indent=2, ensure_ascii=False))
    with ZipFile(out) as archive:
        assert archive.testzip() is None
        for name, digest in hashes.items():
            assert hashlib.sha256(archive.read(name)).hexdigest() == digest
    print(json.dumps({'path': str(out), 'files': len(hashes), 'sha256': hashlib.sha256(out.read_bytes()).hexdigest()}, ensure_ascii=False))
    return out

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('label', nargs='?', default='checkpoint')
    checkpoint(parser.parse_args().label)
