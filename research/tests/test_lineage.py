"""Regression checks for real evidence, rejection paths, and honest readiness status."""
import contextlib
import copy
import io
import json
from pathlib import Path
import shutil
import tempfile
import unittest
from unittest.mock import patch

import pandas as pd
from pypdf import PdfReader

from gidh_delhi_air.evidence import EvidenceError, PROJECT_ROOT, source_path
from gidh_delhi_air.ingest.iari_fires import extract_iari, parse_daily_pages, ingest_iari_district_fires
from gidh_delhi_air.ingest.cpcb_apportionment import extract_apportionment, parse_apportionment_page
from gidh_delhi_air.ingest.fetch_pib_bulletins import parse_pib_bulletin
from gidh_delhi_air.loader import load_iari_district_fires, load_iitk_apportionment
from gidh_delhi_air.verify import verify, validate_telemetry, main


class PrimaryEvidenceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        reader = PdfReader(source_path('iari_paddy_2025_77'))
        cls.pages = [(p, reader.pages[p-1].extract_text(extraction_mode='layout')) for p in (25, 26, 27)]
        cls.daily, cls.annual = extract_iari()
        reader = PdfReader(source_path('iitk_dpcc_2016'))
        cls.winter = reader.pages[292].extract_text(extraction_mode='layout')

    def test_primary_totals_and_daily_scope(self):
        self.assertEqual(len(self.daily), 1386)
        self.assertEqual(len(self.annual), 18)
        totals = self.annual.set_index(['state', 'year']).total_fire_incidents
        self.assertEqual(totals['Punjab', 2020], 83002)
        self.assertEqual(totals['Haryana', 2020], 4202)
        self.assertEqual(totals['Punjab', 2024], 10909)
        self.assertEqual(totals['Uttar Pradesh', 2025], 7290)
        self.assertEqual(set(self.daily.geographic_scope), {'whole_state'})
        self.assertEqual(set(self.daily.source_pdf_page), {25, 26, 27})

    def test_daily_missing_date_rejected(self):
        pages = copy.deepcopy(self.pages)
        pages[0] = (25, '\n'.join(l for l in pages[0][1].splitlines() if not l.strip().startswith('15-Sep')))
        with self.assertRaisesRegex(EvidenceError, '77 dates'):
            parse_daily_pages(pages)

    def test_daily_duplicate_date_rejected(self):
        line = next(l for l in self.pages[0][1].splitlines() if l.strip().startswith('15-Sep'))
        pages = [(25, self.pages[0][1] + '\n' + line)] + self.pages[1:]
        with self.assertRaisesRegex(EvidenceError, 'Duplicate'):
            parse_daily_pages(pages)

    def test_daily_missing_total_rejected(self):
        with self.assertRaisesRegex(EvidenceError, '77 dates'):
            parse_daily_pages(self.pages[:2])

    def test_daily_does_not_reconcile_rejected(self):
        pages = self.pages[:2] + [(27, self.pages[2][1].replace('83002', '83003'))]
        with self.assertRaisesRegex(EvidenceError, 'mismatch'):
            parse_daily_pages(pages)

    def test_daily_wrong_column_count_rejected(self):
        pages = [(25, '15-Sep 1 2 3')] + self.pages[1:]
        with self.assertRaisesRegex(EvidenceError, 'Malformed'):
            parse_daily_pages(pages)

    def test_apportionment_exact_categories_and_precision(self):
        frame = extract_apportionment()
        self.assertEqual(len(frame), 18)
        row = frame[(frame.season == 'Winter') & (frame.source_sector == 'Biomass burning')].iloc[0]
        self.assertEqual(row.share_percentage, 25.84)
        self.assertEqual(row.source_table, '4.20(b)')
        self.assertEqual(row.source_pdf_page, 293)
        self.assertEqual(row.source_printed_page, 248)
        self.assertAlmostEqual(frame[frame.season == 'Summer'].share_percentage.sum(), 100.10)
        self.assertNotIn('Others', set(frame.source_sector))
        self.assertNotIn('primary_chemical_marker', frame.columns)

    def test_apportionment_wrong_table_rejected(self):
        with self.assertRaisesRegex(EvidenceError, 'Missing'):
            parse_apportionment_page(self.winter, 'Winter', 293, '248', '9.99')

    def test_apportionment_missing_overall_rejected(self):
        with self.assertRaisesRegex(EvidenceError, 'Overall'):
            parse_apportionment_page(self.winter.replace('Overall', 'Missing'), 'Winter', 293, '248', '4.20(b)')

    def test_apportionment_invalid_share_rejected(self):
        with self.assertRaisesRegex(EvidenceError, 'Invalid'):
            parse_apportionment_page(self.winter.replace('29.88', '129.88'), 'Winter', 293, '248', '4.20(b)')

    def test_retired_apis_never_emit_official_data(self):
        for call in [lambda: load_iari_district_fires(PROJECT_ROOT / 'data/quarantine'),
                     lambda: ingest_iari_district_fires(Path('/tmp')),
                     lambda: parse_pib_bulletin(2025, Path('/missing.html'))]:
            with self.assertRaises(EvidenceError):
                call()

    def test_loader_rejects_modified_benchmark(self):
        with tempfile.TemporaryDirectory() as tmp:
            frame = extract_apportionment()
            frame.loc[0, 'share_percentage'] = 1
            frame.to_csv(Path(tmp) / 'iitk_dpcc_pm25_apportionment.csv', index=False)
            with self.assertRaisesRegex(EvidenceError, 'primary evidence'):
                load_iitk_apportionment(Path(tmp))


class TelemetryChecks(unittest.TestCase):
    def setUp(self):
        self.stations = pd.DataFrame({'station_id': [1, 2]})
        self.sources = pd.DataFrame({
            'source_file_id': [10, 11], 'station_id': [1, 1], 'source_type': ['CAAQMS', 'AQI'],
            'processing_status': ['loaded', 'loaded'], 'row_count': [1, 1],
            'reporting_period_start': ['2025-01-01T00:00:00+05:30'] * 2,
            'reporting_period_end': ['2025-01-01T00:00:00+05:30'] * 2,
        })
        self.frames = {
            name: pd.DataFrame({'station_id': [1], 'source_file_id': [sid],
                                'timestamp': ['2025-01-01T00:00:00+05:30'], 'qc_flags': ['{}']})
            for name, sid in [('caaqms_hourly', 10), ('aqi_hourly', 11)]}

    def test_valid_sparse_coverage_reported(self):
        report = validate_telemetry(self.stations, self.sources, self.frames)
        self.assertEqual(report['caaqms_hourly']['coverage_by_station_year'][0]
                         ['hours_without_rows_in_calendar_year'], 8759)
        absent = report['caaqms_hourly']['coverage_by_station_year'][1]
        self.assertEqual(absent['rows'], 0)
        self.assertIsNone(absent['first_timestamp'])

    def test_foreign_keys_and_station_match(self):
        for field, value, error in [('source_file_id', 99, 'unknown source'),
                                    ('station_id', 2, 'station mismatch')]:
            frames = copy.deepcopy(self.frames)
            frames['caaqms_hourly'].loc[0, field] = value
            with self.subTest(field=field), self.assertRaisesRegex(EvidenceError, error):
                validate_telemetry(self.stations, self.sources, frames)

    def test_duplicate_hours_rejected(self):
        self.frames['caaqms_hourly'] = pd.concat([self.frames['caaqms_hourly']] * 2)
        with self.assertRaisesRegex(EvidenceError, 'duplicate'):
            validate_telemetry(self.stations, self.sources, self.frames)

    def test_bad_counts_rejected(self):
        self.sources.loc[0, 'row_count'] = 2
        with self.assertRaisesRegex(EvidenceError, 'row count'):
            validate_telemetry(self.stations, self.sources, self.frames)

    def test_wrong_timezone_rejected(self):
        self.frames['caaqms_hourly'].loc[0, 'timestamp'] = '2025-01-01T00:00:00Z'
        with self.assertRaisesRegex(EvidenceError, 'timezone'):
            validate_telemetry(self.stations, self.sources, self.frames)

    def test_bad_qc_rejected(self):
        self.frames['caaqms_hourly'].loc[0, 'qc_flags'] = '[]'
        with self.assertRaisesRegex(EvidenceError, 'JSON objects'):
            validate_telemetry(self.stations, self.sources, self.frames)


class VerificationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temp = tempfile.TemporaryDirectory()
        cls.root = Path(cls.temp.name)
        shutil.copytree(PROJECT_ROOT / 'data', cls.root / 'data')
        cls.baseline = verify(cls.root)

    @classmethod
    def tearDownClass(cls):
        cls.temp.cleanup()

    def test_integrity_pass_does_not_sign_off(self):
        self.assertEqual(self.baseline['errors'], [])
        self.assertTrue(self.baseline['integrity_passed'])
        self.assertFalse(self.baseline['milestone_complete'])
        self.assertEqual(len(self.baseline['blockers']), 3)
        self.assertEqual(self.baseline['checks']['telemetry_archive_byte_matches'], 5)

    def test_cli_exit_codes_preserve_blockers(self):
        for integrity_only, code in [(False, 1), (True, 0)]:
            args = ['--json'] + (['--integrity-only'] if integrity_only else [])
            with patch('gidh_delhi_air.verify.verify', return_value=self.baseline), contextlib.redirect_stdout(io.StringIO()) as out:
                self.assertEqual(main(args), code)
            self.assertFalse(json.loads(out.getvalue())['milestone_complete'])
        bad = dict(self.baseline, integrity_passed=False, errors=['tampered'])
        with patch('gidh_delhi_air.verify.verify', return_value=bad), contextlib.redirect_stdout(io.StringIO()):
            self.assertEqual(main(['--integrity-only']), 2)

    def test_missing_primary_evidence_fails(self):
        path = self.root / 'data/primary_sources/iari_paddy_bulletin_77_2025-11-30.pdf'
        moved = path.with_suffix('.hold')
        path.rename(moved)
        try:
            result = verify(self.root)
            self.assertFalse(result['integrity_passed'])
            self.assertIn('Missing evidence', result['errors'][0])
        finally:
            moved.rename(path)

    def test_primary_tampering_fails(self):
        path = self.root / 'data/primary_sources/kaggle_dataset_metadata.json'
        original = path.read_bytes()
        try:
            path.write_bytes(original + b' ')
            result = verify(self.root)
            self.assertFalse(result['integrity_passed'])
            self.assertIn('checksum mismatch', result['errors'][0])
        finally:
            path.write_bytes(original)

    def test_removing_blockers_is_not_evidence(self):
        path = self.root / 'data/source_manifest.json'
        original = path.read_bytes()
        try:
            manifest = json.loads(original)
            manifest['unresolved_requirements'] = []
            path.write_text(json.dumps(manifest))
            result = verify(self.root)
            self.assertFalse(result['integrity_passed'])
            self.assertFalse(result['milestone_complete'])
            self.assertIn('acceptance requirements', result['errors'][0])
        finally:
            path.write_bytes(original)

    def test_telemetry_tampering_fails(self):
        path = self.root / 'data/delhi_air_quality_monitoring_dataset/stations.csv'
        original = path.read_bytes()
        try:
            path.write_bytes(original + b'\n')
            result = verify(self.root)
            self.assertFalse(result['integrity_passed'])
            self.assertIn('differs from pinned archive', result['errors'][0])
        finally:
            path.write_bytes(original)

    def test_derived_value_tampering_fails(self):
        path = self.root / 'data/indian_official_sources/caqm_stubble_burning_annual_totals.csv'
        original = path.read_bytes()
        try:
            path.write_text(path.read_text().replace('83002', '76590'))
            self.assertFalse(verify(self.root)['integrity_passed'])
        finally:
            path.write_bytes(original)

    def test_legacy_file_reintroduction_fails(self):
        path = self.root / 'data/indian_official_sources/iari_district_daily_stubble_fires.csv'
        path.write_text('fake\n')
        try:
            self.assertFalse(verify(self.root)['integrity_passed'])
        finally:
            path.unlink()


if __name__ == '__main__':
    unittest.main()
