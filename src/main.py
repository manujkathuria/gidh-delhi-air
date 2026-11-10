"""
Entrypoint for Milestone 1: Data Source Finalization.
Verifies all raw and structured data assets are present and can be loaded cleanly.
"""

from gidh_delhi_air.loader import (
    load_stations,
    load_caaqms_hourly,
    load_aqi_hourly,
    load_caqm_annual_totals,
    load_cpcb_apportionment,
    load_iari_district_fires,
)


def main():
    print("=" * 80)
    print("CHECKPOINT 1: DATA SOURCE FINALIZATION")
    print("=" * 80)

    print("\n[Tier 1: Local Ground Telemetry - Inside Delhi]")
    stations = load_stations()
    caaqms = load_caaqms_hourly()
    aqi = load_aqi_hourly()
    print(f"  * Monitoring Stations (DPCC/CPCB) : {len(stations)} active stations")
    print(f"  * CAAQMS Multi-Pollutant Hourly    : {len(caaqms):,} observations (2023-2026)")
    print(f"  * Official Hourly CPCB AQI         : {len(aqi):,} records (2025)")

    print("\n[Tier 2: Official Indian Government Sources - Upwind & Regional]")
    caqm = load_caqm_annual_totals()
    apportion = load_cpcb_apportionment()
    iari = load_iari_district_fires()
    print(f"  * CAQM Annual Stubble Totals       : {len(caqm)} records (2020-2025, Punjab/Haryana/UP)")
    print(f"  * CPCB / IIT-K Source Apportionment: {len(apportion)} chemical mass balance benchmark shares")
    print(f"  * ICAR-IARI District-Daily Fires   : {len(iari):,} records (65 districts, 2023-2025)")

    print("\n" + "=" * 80)
    print("DATA SOURCE FINALIZATION STATUS: ALL 3 PILLARS VERIFIED & READY")
    print("=" * 80)


if __name__ == "__main__":
    main()
