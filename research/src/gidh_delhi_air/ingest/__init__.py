"""Rebuild source-backed records from pinned local evidence; no network fallback."""
from pathlib import Path
from gidh_delhi_air.evidence import PROJECT_ROOT
from gidh_delhi_air.paths import PATHS
from gidh_delhi_air.ingest.cpcb_apportionment import extract_apportionment, OUTPUT_FILE
from gidh_delhi_air.ingest.iari_fires import extract_iari, DAILY_FILE, ANNUAL_FILE

DEFAULT_OUTPUT_DIR = PATHS.reference


def run_all_ingest(output_dir: Path = DEFAULT_OUTPUT_DIR) -> dict[str, Path]:
    # Parse every source before writing, so missing evidence cannot publish a partial rebuild.
    daily, annual = extract_iari()
    apportionment = extract_apportionment()
    output_dir.mkdir(parents=True, exist_ok=True)
    result = {}
    for name, filename, frame in (('state_daily', DAILY_FILE, daily),
                                  ('annual_totals', ANNUAL_FILE, annual),
                                  ('apportionment', OUTPUT_FILE, apportionment)):
        path = output_dir / filename
        frame.to_csv(path, index=False)
        result[name] = path
        print(f'Rebuilt {path.name}: {len(frame):,} source-backed rows')
    return result
