"""Verify a source checkpoint and restore it into a new directory only."""
import argparse
import hashlib
import json
from pathlib import Path, PurePosixPath
from zipfile import ZipFile


def restore(archive_path, destination):
    destination=Path(destination)
    if destination.exists():
        raise FileExistsError('Restore destination must be new')
    with ZipFile(archive_path) as archive:
        names=archive.namelist()
        if len(names)!=len(set(names)):
            raise ValueError('Duplicate archive entries')
        hashes=json.loads(archive.read('CHECKPOINT_MANIFEST.json'))
        if set(names)!=set(hashes)|{'CHECKPOINT_MANIFEST.json'}:
            raise ValueError('Manifest and archive differ')
        contents={}
        for name,digest in hashes.items():
            relative=PurePosixPath(name)
            if relative.is_absolute() or '..' in relative.parts or '\\' in name or ':' in name:
                raise ValueError('Unsafe archive path')
            info=archive.getinfo(name)
            if (info.external_attr>>16)&0o170000==0o120000:
                raise ValueError('Archive links are not allowed')
            data=archive.read(name)
            if hashlib.sha256(data).hexdigest()!=digest:
                raise ValueError('Checksum mismatch: '+name)
            contents[name]=data
    destination.mkdir(parents=True,exist_ok=False)
    for name,data in contents.items():
        target=destination/name
        if not target.resolve().is_relative_to(destination.resolve()):
            raise ValueError('Destination escaped')
        target.parent.mkdir(parents=True,exist_ok=True)
        with target.open('xb') as stream:
            stream.write(data)
    return len(contents)


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('archive')
    parser.add_argument('destination')
    args=parser.parse_args()
    print(json.dumps({'restored_files':restore(args.archive,args.destination),'destination':str(Path(args.destination).resolve())},ensure_ascii=False))
