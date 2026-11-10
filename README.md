# GIDH Delhi Air Quality Analysis

**Milestone 1:** Data Source Finalization & Lineage Verification  
**Objective:** Establish and finalize official, verifiable empirical data sources for Delhi air quality and regional pollution source attribution without premature analytical assumptions.

---

## Finalized Data Architecture (The 3 Pillars)

### Pillar 1: Local Ground Telemetry (Inside Delhi)
* **Issuing Bodies:** Delhi Pollution Control Committee (DPCC) & Central Pollution Control Board (CPCB).
* **Dataset:** 162,096 continuous hourly CAAQMS multi-pollutant observations + 57,946 hourly official AQI records across 7 monitoring stations (2023–2026).
* **Storage Location:** `data/delhi_air_quality_monitoring_dataset/`

### Pillar 2: Upwind Agricultural Residue Burning (Regional Plains)
* **Issuing Bodies:** Commission for Air Quality Management in NCR (CAQM) & ICAR - Indian Agricultural Research Institute (CREAMS Laboratory, Pusa, New Delhi).
* **Dataset:** 
  * Annual audit totals from 2020 through 2025 for Punjab, Haryana, and Uttar Pradesh (CAQM / PIB official releases).
  * 15,015 district-daily satellite active fire records across 65 agricultural districts for the full harvest season (Sep 15 – Nov 30) across 2023, 2024, and 2025.
* **Storage Locations:** `data/indian_official_sources/` and raw HTML bulletins in `data/raw_bulletins/`.

### Pillar 3: Chemical Source Apportionment Benchmarks (Delhi Speciation)
* **Issuing Bodies:** Indian Institute of Technology (IIT) Kanpur for DPCC & CPCB.
* **Study:** *Comprehensive Study on Air Pollution and Green House Gases in Delhi* (Prof. Mukesh Sharma & Prof. Onkar Dikshit).
* **Dataset:** Filter-based Chemical Mass Balance (CMB) seasonal percentage shares for fine particulate matter ($PM_{2.5}$).
* **Storage Location:** `data/indian_official_sources/cpcb_iitk_source_apportionment.csv`

---

## Documentation
* **[Official Data Provenance & Primary Source Registry](docs/data_provenance_and_citations.md):** The single source of truth detailing primary issuing authorities, permanent portal URLs, statutory Press Release IDs (PRIDs), physical instruments, and collection methodologies.

---

## Quickstart

Verify all finalized data sources:
```bash
uv run python src/main.py
```

Re-run official Indian data ingestion from raw bulletins:
```bash
uv run python -m gidh_delhi_air.ingest
```
