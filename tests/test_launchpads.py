import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
import kit


class LaunchpadTests(unittest.TestCase):
    def setUp(self):
        (kit.ROOT / 'work' / '_tests').mkdir(parents=True, exist_ok=True)
        self.temp = tempfile.TemporaryDirectory(dir=kit.ROOT / 'work' / '_tests')
        self.addCleanup(self.temp.cleanup)

    def test_every_profile_generates_without_network(self):
        with patch('kit.subprocess.run') as run:
            for p in kit.read('launchpads.json'):
                dest = kit.prepare(p['id'], p['id'], self.temp.name)
                self.assertTrue((dest / 'START_HERE.md').exists())
                self.assertTrue((dest / 'INTENT.md').exists())
                self.assertFalse((dest / 'upstream').exists())
            run.assert_not_called()
        self.assertTrue((Path(self.temp.name) / 'local/.devcontainer/devcontainer.json').exists())

    def test_fetch_records_commit_and_never_runs_install(self):
        with patch('kit.subprocess.run') as run, patch('kit.subprocess.check_output', return_value='abc123\n'):
            dest = kit.prepare('web', 'sample', self.temp.name, fetch=True)
        run.assert_called_once_with(['git', 'clone', '--depth', '1', 'https://github.com/fastapi/full-stack-fastapi-template.git', str(dest / 'upstream')], check=True)
        self.assertEqual((dest / 'UPSTREAM_COMMIT.txt').read_text().strip(), 'abc123')

    def test_unknown_traversal_and_existing_are_rejected(self):
        with self.assertRaises(ValueError):
            kit.prepare('missing', 'sample', self.temp.name)
        with self.assertRaises(ValueError):
            kit.prepare('web', '../outside', self.temp.name)
        kit.prepare('web', 'existing', self.temp.name)
        with self.assertRaises(FileExistsError):
            kit.prepare('web', 'existing', self.temp.name)
