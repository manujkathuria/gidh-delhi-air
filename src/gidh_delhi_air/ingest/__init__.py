"""
Master ingestion orchestrator for Indian official external datasets.
Executes individual provider ingestion modules and populates data/indian_official_sources/
"""

from pathlib import Path
from gidh_delhi_air.ingest.fetch_pib_bulletins import run_pib_fetcher
from gidh_delhi_air.ingest.cpcb_apportionment import ingest_cpcb_apportionment
from gidh_delhi_air.ingest.iari_fires import ingest_iari_district_fires

DEFAULT_OUTPUT_DIR = Path(__file__).resolve().parents[3] / "data" / "indian_official_sources"


def run_all_ingest(output_dir: Path = DEFAULT_OUTPUT_DIR) -> dict[str, Path]:
    print("=" * 80)
    print("STARTING INGESTION PIPELINE: OFFICIAL INDIAN GOVERNMENT DATA")
    print("=" * 80)

    results = {}

    print("\n[1/3] Downloading & Parsing Raw PIB Bulletins for CAQM Annual Totals (2020-2025)...")
    path_caqm = run_pib_fetcher()
    results["caqm_totals"] = path_caqm
    print(f"  -> Generated: {path_caqm}")

    print("\n[2/3] Ingesting CPCB / IIT Kanpur Chemical Source Apportionment Benchmarks...")
    path_cpcb = ingest_cpcb_apportionment(output_dir)
    results["cpcb_apportionment"] = path_cpcb
    print(f"  -> Generated: {path_cpcb}")

    print("\n[3/3] Ingesting ICAR-IARI District-Daily Stubble Burning Telemetry (65 Districts, 2023-2025)...")
    path_iari = ingest_iari_district_fires(output_dir)
    results["iari_district_fires"] = path_iari
    print(f"  -> Generated: {path_iari}")

    print("\n" + "=" * 80)
    print("INGESTION COMPLETE: ALL OFFICIAL INDIAN DATASETS POPULATED SUCCESSFULLY")
    print("=" * 80)
    return results


if __name__ == "__main__":
    run_all_ingest()
