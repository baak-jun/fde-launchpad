import hashlib
import importlib.util
import json
import tempfile
import unittest
from pathlib import Path
from zipfile import ZipFile

ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('restore_checkpoint',ROOT/'scripts/restore_checkpoint.py')
module=importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


class RestoreTests(unittest.TestCase):
    def setUp(self):
        base=ROOT/'work/_tests'
        base.mkdir(parents=True,exist_ok=True)
        self.tmp=tempfile.TemporaryDirectory(dir=base)
        self.root=Path(self.tmp.name)

    def tearDown(self):
        self.tmp.cleanup()

    def archive(self,name='src/example.txt',bad_hash=False):
        path=self.root/'source.zip'
        data='보존할 원본'.encode()
        with ZipFile(path,'w') as out:
            out.writestr(name,data)
            out.writestr('CHECKPOINT_MANIFEST.json',json.dumps({name:'wrong' if bad_hash else hashlib.sha256(data).hexdigest()}))
        return path

    def test_roundtrip_and_existing_destination_protection(self):
        archive=self.archive()
        dest=self.root/'new'
        self.assertEqual(module.restore(archive,dest),1)
        self.assertEqual((dest/'src/example.txt').read_text(encoding='utf-8'),'보존할 원본')
        with self.assertRaises(FileExistsError):
            module.restore(archive,dest)

    def test_path_escape_rejected_before_writing(self):
        with self.assertRaises(ValueError):
            module.restore(self.archive('../outside.txt'),self.root/'new')
        self.assertFalse((self.root/'new').exists())

    def test_modified_data_rejected_before_writing(self):
        with self.assertRaises(ValueError):
            module.restore(self.archive(bad_hash=True),self.root/'new')
        self.assertFalse((self.root/'new').exists())
