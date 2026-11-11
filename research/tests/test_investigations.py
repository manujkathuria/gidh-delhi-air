"""Research structure contracts: isolation, honest planning and CLI configuration."""
import contextlib
import io
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

from gidh_delhi_air.evidence import PROJECT_ROOT, read_manifest
from gidh_delhi_air.investigations.__main__ import main
from gidh_delhi_air.investigations.clean_days.config import CleanDaysConfig
from gidh_delhi_air.investigations.models import AnalysisPlan, Investigation
from gidh_delhi_air.investigations.registry import (
    INVESTIGATIONS, Registration, list_investigations, plan_investigation,
)
from gidh_delhi_air.paths import ProjectPaths, find_project_root


class LayoutTests(unittest.TestCase):
    def test_root_discovery_uses_workspace_not_evidence_availability(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / 'research/src/nested').mkdir(parents=True)
            (root / 'research/pyproject.toml').write_text('[project]\n')
            (root / 'package.json').write_text('{}')
            self.assertEqual(find_project_root(root / 'research/src/nested'), root.resolve())
            # Missing datasets must not break root discovery or help/plan imports.
            self.assertFalse((root / 'data/source_manifest.json').exists())

    def test_unknown_workspace_reports_actionable_error(self):
        with tempfile.TemporaryDirectory() as tmp:
            with self.assertRaisesRegex(FileNotFoundError, 'source checkout'):
                find_project_root(Path(tmp))

    def test_paths_are_isolated_and_do_not_create_directories(self):
        with tempfile.TemporaryDirectory() as tmp:
            paths = ProjectPaths(Path(tmp))
            first = paths.investigation_processed('clean-days')
            second = paths.investigation_processed('diwali')
            self.assertNotEqual(first, second)
            self.assertNotEqual(paths.investigation_published('clean-days'), first)
            self.assertEqual(list(Path(tmp).iterdir()), [])
            for value in ('../raw', '/tmp', '', 'Clean Days', 'clean_days'):
                with self.subTest(value=value), self.assertRaises(ValueError):
                    paths.investigation_published(value)


class InvestigationTests(unittest.TestCase):
    def test_plan_is_read_only_and_preserves_lineage(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / 'data').mkdir()
            (root / 'data/source_manifest.json').write_text(json.dumps(read_manifest()))
            before = {p.relative_to(root) for p in root.rglob('*')}
            plan = plan_investigation('clean-days', paths=ProjectPaths(root))
            self.assertEqual({p.relative_to(root) for p in root.rglob('*')}, before)
            self.assertFalse(plan.results_available)
            self.assertEqual(plan.investigation.status, 'planning')
            self.assertIsNone(plan.parameters['min_valid_hours_per_day'])
            self.assertIsNone(plan.parameters['multi_station_rule'])
            self.assertEqual(len(plan.inputs), 2)
            self.assertTrue(all(len(entry['sha256']) == 64 for entry in plan.inputs))
            self.assertEqual(plan.outputs['publication_status'], 'not_generated')
            self.assertEqual(plan.to_dict()['schema_version'], 1)

    def test_json_config_normalizes_station_ids_and_validates_coverage(self):
        plan = plan_investigation('clean-days', {'year': 2024, 'target_days': 20, 'station_ids': [3, 5]})
        self.assertEqual(plan.parameters['station_ids'], (3, 5))
        self.assertIn('20', plan.investigation.title)
        for parameters in ({'year': 2026}, {'target_days': 0}, {'target_days': True},
                           {'station_ids': [3, 3]}, {'station_ids': [99]}, {'unexpected': 1}):
            with self.subTest(parameters=parameters), self.assertRaises(ValueError):
                plan_investigation('clean-days', parameters)
        with self.assertRaisesRegex(ValueError, 'Unknown investigation'):
            plan_investigation('unknown')

    def test_config_cannot_be_changed_after_validation(self):
        ids = [3, 4]
        config = CleanDaysConfig(station_ids=ids)
        ids.append(99)
        self.assertEqual(config.station_ids, (3, 4))

    def test_new_investigation_uses_registry_without_cli_dispatch_changes(self):
        definition = Investigation('example', 'Example', 'A future question?', 'planning')
        def planner(parameters, paths):
            return AnalysisPlan(definition, parameters, (), {}, (), ())
        with patch.dict(INVESTIGATIONS, {'example': Registration(definition, planner)}):
            self.assertIn('example', {item.id for item in list_investigations()})
            with contextlib.redirect_stdout(io.StringIO()) as out:
                self.assertEqual(main(['plan', 'example', '--set', 'window=7', '--json']), 0)
            result = json.loads(out.getvalue())
            self.assertEqual(result['investigation']['id'], 'example')
            self.assertEqual(result['parameters']['window'], 7)

    def test_cli_config_and_overrides(self):
        with tempfile.TemporaryDirectory() as tmp:
            config = Path(tmp) / 'config.json'
            config.write_text(json.dumps({'year': 2024, 'target_days': 10}))
            with contextlib.redirect_stdout(io.StringIO()) as out:
                self.assertEqual(main(['plan', 'clean-days', '--config', str(config),
                                       '--set', 'target_days=30', '--json']), 0)
            result = json.loads(out.getvalue())
            self.assertEqual(result['parameters']['year'], 2024)
            self.assertEqual(result['parameters']['target_days'], 30)
            self.assertFalse(result['results_available'])

    def test_cli_rejects_bad_configuration_with_nonzero_exit(self):
        for arguments in (['plan', 'unknown'], ['plan', 'clean-days', '--set', 'year=2026'],
                          ['plan', 'clean-days', '--set', 'broken'],
                          ['plan', 'clean-days', '--set', 'target_days=abc']):
            with self.subTest(arguments=arguments), contextlib.redirect_stderr(io.StringIO()):
                with self.assertRaises(SystemExit) as error:
                    main(arguments)
                self.assertEqual(error.exception.code, 2)

    def test_cli_works_from_another_working_directory(self):
        result = subprocess.run(
            [sys.executable, '-m', 'gidh_delhi_air.investigations', 'plan', 'clean-days', '--json'],
            cwd=tempfile.gettempdir(), capture_output=True, text=True, check=True,
        )
        self.assertEqual(json.loads(result.stdout)['inputs'][0]['source_id'], 'kaggle_telemetry_v1')
        self.assertTrue((PROJECT_ROOT / 'research/pyproject.toml').is_file())


if __name__ == '__main__':
    unittest.main()
