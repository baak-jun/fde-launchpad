import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('kit', ROOT / 'kit.py')
kit = importlib.util.module_from_spec(spec)
spec.loader.exec_module(kit)

class KitTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temp_root = ROOT / 'work' / '_tests'
        cls.temp_root.mkdir(parents=True, exist_ok=True)

    def test_recipes_reference_known_repos_and_have_acceptance(self):
        rows = kit.read('repos.json')
        names = {r['repo'] for r in rows}
        self.assertEqual(len(names), 28)
        for recipe in kit.read('recipes.json'):
            self.assertTrue(set(recipe['repos'] + recipe['optional']) <= names)
            self.assertTrue(recipe['acceptance'])

    def test_generate_every_recipe_and_keep_unknown_results_unknown(self):
        with tempfile.TemporaryDirectory(dir=self.temp_root) as folder:
            for recipe in kit.read('recipes.json'):
                dest = kit.scaffold(recipe['id'], recipe['id'], folder)
                self.assertNotIn('{{', (dest / 'BRIEF.md').read_text(encoding='utf-8'))
                evaluation = json.loads((dest / 'EVALUATION.json').read_text(encoding='utf-8'))
                self.assertEqual(evaluation['status'], 'template_not_executed')
                self.assertIsNone(evaluation['measurements']['task_success_rate'])

    def test_does_not_overwrite_existing_project(self):
        with tempfile.TemporaryDirectory(dir=self.temp_root) as folder:
            dest = kit.scaffold('triage', 'existing', folder)
            marker = dest / 'BRIEF.md'
            marker.write_text('user work', encoding='utf-8')
            with self.assertRaises(FileExistsError):
                kit.scaffold('triage', 'existing', folder)
            self.assertEqual(marker.read_text(encoding='utf-8'), 'user work')

    def test_rejects_escape_paths_and_reserved_names(self):
        with tempfile.TemporaryDirectory(dir=self.temp_root) as folder:
            for name in ['../escape', 'a/b', 'a\\b', 'C:\\escape', 'con', 'lpt1', '']:
                with self.subTest(name=name), self.assertRaises(ValueError):
                    kit.scaffold('triage', name, folder)
            self.assertEqual(list(Path(folder).iterdir()), [])

    def test_unknown_recipe_creates_nothing(self):
        with tempfile.TemporaryDirectory(dir=self.temp_root) as folder:
            with self.assertRaises(ValueError):
                kit.scaffold('missing', 'example', folder)
            self.assertEqual(list(Path(folder).iterdir()), [])

    def test_source_evidence_is_complete(self):
        for row in kit.read('repos.json'):
            folder = ROOT / 'evidence/github' / row['source_repo'].replace('/', '__')
            for name in ['readme.txt', 'license.txt', 'metadata.json']:
                self.assertTrue((folder / name).is_file(), str(folder / name))
            self.assertFalse(row['archived'])

    def test_starter_is_self_contained_and_excludes_local_data(self):
        with tempfile.TemporaryDirectory(dir=self.temp_root) as folder:
            dest = kit.start_project('portable', folder)
            for name in ['run_workbench.py','requirements.lock','runtime/app.py','domain_packs/support.json','HANDOFF.md','skills/fde-workbench-flow/SKILL.md']:
                self.assertTrue((dest/name).is_file())
            for name in ['.venv','runtime-data','.env','.git','backups']:
                self.assertFalse((dest/name).exists())
            with self.assertRaises(FileExistsError):
                kit.start_project('portable',folder)

if __name__ == '__main__':
    unittest.main()
