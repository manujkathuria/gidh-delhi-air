"""Check evidence integrity and record consistency without claiming scientific validity."""
import argparse
import json
from pathlib import Path
import zipfile
import hashlib

import pandas as pd
from pandas.testing import assert_frame_equal

from gidh_delhi_air.evidence import EvidenceError, PROJECT_ROOT, read_manifest, source_path
from gidh_delhi_air.paths import ProjectPaths
from gidh_delhi_air.ingest.iari_fires import extract_iari, DAILY_FILE, ANNUAL_FILE
from gidh_delhi_air.ingest.cpcb_apportionment import extract_apportionment, OUTPUT_FILE

# Current acceptance boundary. Clearing manifest prose cannot establish new evidence.
REQUIRED_GAPS = {'telemetry_primary_lineage', 'district_daily_observations', 'telemetry_license'}

def require(condition: bool, message: str) -> None:
    if not condition:
        raise EvidenceError(message)


def validate_telemetry(stations: pd.DataFrame, sources: pd.DataFrame,
                       frames: dict[str, pd.DataFrame]) -> dict:
    """Validate publisher IDs/windows; describe gaps rather than infer their cause."""
    require(stations.station_id.notna().all() and stations.station_id.is_unique,
            'Station identifiers must be present and unique')
    require(sources.source_file_id.notna().all() and sources.source_file_id.is_unique,
            'Source file identifiers must be present and unique')
    require(sources.station_id.isin(stations.station_id).all(), 'Unknown station in source registry')
    require(sources.source_type.isin(['CAAQMS', 'AQI']).all(), 'Unknown telemetry source type')
    require(sources.processing_status.eq('loaded').all(), 'Unloaded source in telemetry registry')
    all_source_ids = set()
    result = {}
    for name, frame in frames.items():
        expected_type = {'caaqms_hourly': 'CAAQMS', 'aqi_hourly': 'AQI'}[name]
        keys = ['station_id', 'source_file_id', 'timestamp']
        require(not frame[keys].isna().any().any(), f'{name}: null lineage key')
        require(frame.station_id.isin(stations.station_id).all(), f'{name}: unknown station')
        require(not frame.duplicated(['station_id', 'timestamp']).any(), f'{name}: duplicate station/time')
        require(frame.source_file_id.isin(sources.source_file_id).all(), f'{name}: unknown source file')
        # Preserve source-local time semantics, including explicit +05:30 offsets.
        require(frame.timestamp.astype(str).str.endswith('+05:30').all(), f'{name}: wrong/missing timezone')
        ts = pd.to_datetime(frame.timestamp, errors='raise')
        require((ts.dt.minute.eq(0) & ts.dt.second.eq(0)).all(), f'{name}: non-hourly timestamp')
        joined = frame.merge(sources, on='source_file_id', suffixes=('', '_source'), validate='many_to_one')
        require(joined.station_id.eq(joined.station_id_source).all(), f'{name}: source station mismatch')
        require(joined.source_type.eq(expected_type).all(), f'{name}: source type mismatch')
        counts = frame.groupby('source_file_id').size()
        registry = sources[sources.source_type == expected_type].set_index('source_file_id')
        require(set(counts.index) == set(registry.index), f'{name}: missing/unexpected source batches')
        require(counts.eq(registry.row_count.reindex(counts.index)).all(), f'{name}: source row count mismatch')
        starts = pd.to_datetime(joined.reporting_period_start)
        ends = pd.to_datetime(joined.reporting_period_end)
        joined_ts = pd.to_datetime(joined.timestamp)
        require(((joined_ts >= starts) & (joined_ts <= ends)).all(), f'{name}: timestamp outside source window')
        observed = frame.assign(parsed_timestamp=ts).groupby('source_file_id').parsed_timestamp.agg(['min', 'max'])
        require(observed['min'].eq(pd.to_datetime(registry.reporting_period_start).reindex(observed.index)).all()
                and observed['max'].eq(pd.to_datetime(registry.reporting_period_end).reindex(observed.index)).all(),
                f'{name}: declared source window disagrees with observations')
        for value in frame.qc_flags.dropna():
            require(isinstance(json.loads(value), dict), f'{name}: QC flags must be JSON objects')
        station_years = []
        work = frame.assign(parsed_timestamp=ts, year=ts.dt.year)
        for station, year in pd.MultiIndex.from_product([
                sorted(stations.station_id), range(int(work.year.min()), int(work.year.max()) + 1)]):
            group = work[(work.station_id == station) & (work.year == year)]
            start = pd.Timestamp(year=int(year), month=1, day=1, tz='Asia/Kolkata')
            end = pd.Timestamp(year=int(year) + 1, month=1, day=1, tz='Asia/Kolkata')
            expected = int((end - start).total_seconds() / 3600)
            station_years.append({
                'station_id': int(station), 'year': int(year), 'rows': len(group),
                'calendar_year_hours': expected, 'hours_without_rows_in_calendar_year': expected - len(group),
                'first_timestamp': group.parsed_timestamp.min().isoformat() if len(group) else None,
                'last_timestamp': group.parsed_timestamp.max().isoformat() if len(group) else None,
                'months_with_rows': sorted(int(m) for m in group.parsed_timestamp.dt.month.unique()),
            })
        numeric = frame.select_dtypes(include='number').drop(columns=['station_id', 'source_file_id'])
        result[name] = {
            'rows': len(frame), 'station_count': int(frame.station_id.nunique()),
            'null_fraction': {c: float(v) for c, v in frame.isna().mean().items()},
            'negative_value_counts': {c: int(v) for c, v in numeric.lt(0).sum().items()},
            'coverage_by_station_year': station_years,
            'coverage_note': 'Calendar-year gaps include unprovided periods; they do not establish sensor outages.',
        }
        all_source_ids.update(counts.index)
    require(all_source_ids == set(sources.source_file_id), 'Unreferenced telemetry source registry entries')
    return result


def verify(root: Path = PROJECT_ROOT) -> dict:
    report = {'integrity_passed': False, 'milestone_complete': False,
              'errors': [], 'blockers': [], 'checks': {}, 'telemetry': {}}
    try:
        manifest = read_manifest(root)
        gaps = manifest['unresolved_requirements']
        require({g['id'] for g in gaps} == REQUIRED_GAPS and len(gaps) == len(REQUIRED_GAPS),
                'Missing/duplicate acceptance requirements; removing blockers is not new evidence')
        report['blockers'] = [g['description'] for g in gaps]
        ids = [entry['source_id'] for entry in manifest['sources']]
        require(len(ids) == len(set(ids)), 'Duplicate evidence source IDs')
        for sid in ids:
            source_path(sid, root)
        report['checks']['evidence_hashes'] = len(ids)
        telemetry = manifest['telemetry']
        archive = source_path(telemetry['source_id'], root)
        with zipfile.ZipFile(archive) as z:
            require({e['archive_member'] for e in telemetry['files']} ==
                    {'stations.csv', 'source_files.csv', 'column_metadata.csv', 'caaqms_hourly.csv', 'aqi_hourly.csv'},
                    'Telemetry manifest must identify all five archive files')
            for entry in telemetry['files']:
                path = (root / entry['path']).resolve()
                require(root.resolve() in path.parents, 'Telemetry path escapes project root')
                local = path.read_bytes()
                member = z.read(entry['archive_member'])
                require(local == member, f"Telemetry differs from pinned archive: {entry['path']}")
                require(hashlib.sha256(local).hexdigest() == entry['sha256'],
                        f"Telemetry checksum mismatch: {entry['path']}")
        report['checks']['telemetry_archive_byte_matches'] = len(telemetry['files'])
        paths = ProjectPaths(root)
        data_dir = paths.telemetry
        stations = pd.read_csv(data_dir / 'stations.csv')
        sources = pd.read_csv(data_dir / 'source_files.csv')
        frames = {name: pd.read_csv(data_dir / (name + '.csv'), low_memory=False)
                  for name in ('caaqms_hourly', 'aqi_hourly')}
        report['telemetry'] = validate_telemetry(stations, sources, frames)
        daily, annual = extract_iari(root)
        apportionment = extract_apportionment(root)
        official = paths.reference
        require({p.name for p in official.glob('*.csv')} == {DAILY_FILE, ANNUAL_FILE, OUTPUT_FILE},
                'Unexpected official CSV; unsupported observations must stay quarantined')
        for name, expected in ((DAILY_FILE, daily), (ANNUAL_FILE, annual), (OUTPUT_FILE, apportionment)):
            stored = pd.read_csv(official / name)
            assert_frame_equal(stored, expected, check_dtype=False, check_exact=True)
            report['checks'][name] = {'rows': len(stored), 'matches_primary_extraction': True}
        report['checks']['fire_daily_totals_reconcile'] = True
        report['checks']['apportionment_totals'] = {
            str(k): round(float(v), 2) for k, v in apportionment.groupby('season').share_percentage.sum().items()}
        # These are acceptance gaps, independent of whether every checked byte is consistent.
        report['integrity_passed'] = True
    except (EvidenceError, OSError, ValueError, KeyError, AssertionError, zipfile.BadZipFile) as exc:
        report['errors'].append(f'{type(exc).__name__}: {exc}')
    return report


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description='Verify evidence integrity and Milestone 1 readiness')
    parser.add_argument('--integrity-only', action='store_true',
                        help='Exit 0 for integrity checks while retaining milestone blockers')
    parser.add_argument('--json', action='store_true', help='Print the full machine-readable report')
    parser.add_argument('--report', type=Path, help='Also write the full JSON report to this path')
    args = parser.parse_args(argv)
    report = verify()
    encoded = json.dumps(report, indent=2, allow_nan=False)
    if args.report:
        args.report.write_text(encoded + '\n')
    if args.json:
        print(encoded)
    else:
        print('Evidence integrity: ' + ('PASS' if report['integrity_passed'] else 'FAIL'))
        print('Milestone 1: INCOMPLETE')
        for error in report['errors']:
            print('ERROR: ' + error)
        for blocker in report['blockers']:
            print('BLOCKER: ' + blocker)
        for name, info in report['telemetry'].items():
            print(f"{name}: {info['rows']:,} rows, {info['station_count']} stations")
    if not report['integrity_passed']:
        return 2
    return 0 if args.integrity_only or report['milestone_complete'] else 1


if __name__ == '__main__':
    raise SystemExit(main())
