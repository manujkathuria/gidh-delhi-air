# Source registry and lineage boundaries

This registry records what the project has actually checked. It does not claim ISO/DAMA certification, instrument verification, or milestone completion. Checksums establish the identity of downloaded bytes, not the scientific accuracy of a publication.

## 1. Ground telemetry: verified redistribution, incomplete primary lineage

- Redistributor: Siddharth Dongardive, [Kaggle Delhi Air Quality Monitoring Dataset 2023–2026](https://www.kaggle.com/datasets/siddharthdongardive/delhi-air-quality-monitoring-dataset-2023-2026).
- Pinned version: **1**, dataset ID **12062575**; publisher update timestamp **2026-09-17T12:35:28.527Z**, as reported by the archived Kaggle API metadata.
- Archive: `data/primary_sources/kaggle_telemetry_v1.zip`. Public acquisition URL, acquisition timestamp, SHA-256 and metadata/description snapshots are in `data/source_manifest.json`.
- Local files: `data/delhi_air_quality_monitoring_dataset/{stations,source_files,column_metadata,caaqms_hourly,aqi_hourly}.csv`.
- **All five CSVs match the archive byte for byte.** The project does not alter observations, units, timestamps or publisher QC flags.
- Publisher-attributed upstream authorities: DPCC/CPCB. Their original CSV/XLSX reports are not in this archive. File names and `source_file_id` establish internal linkage, not independently authenticated primary exports.
- Missing upstream evidence: export acquisition records, originals, instrument specifications, unit derivations and transformation/QC source code. The archive's dictionary describes out-of-bounds sentinel nullification; the code/rules responsible have not been obtained.
- License: metadata says **Other (specified in description)**. The archived full dataset description claims derivation under **OGD Platform India terms** and asks users to cite CPCB/DPCC. This is a redistributor claim: applicability to the underlying government exports and permission for the curated redistribution remain unverified. The description links an upstream GitHub project, but that repository returned 404 during this repair; its ETL code was not obtained.

Verification checks station/source key uniqueness, foreign keys, station and source-type agreement, per-file row counts, timestamp offsets and hourly alignment, declared reporting windows, duplicate station/times and QC JSON structure. It reports station/year coverage and per-column missingness.

CAAQMS has 162,096 rows, AQI 57,946, across seven stations (IDs 3–9). CAAQMS 2023 is available only for Dwarka (ID 5); the other stations start in 2024 and end in August 2026, with no July 2026 rows. Dwarka ends in 2025. AQI contains 2025 only. This is an **archive coverage gap**, not a proven simultaneous sensor outage. An hourly row is not necessarily a valid pollutant measurement. Values near 1,000 do not establish instrument saturation without instrument/QC evidence. The publisher dictionary calls source reporting windows UTC although its values use +05:30; interpretation here follows the explicit offsets and the observation timestamp definition.

## 2. Fire observations: IARI primary bulletin

- Issuer: CREAMS Laboratory, Division of Agricultural Physics, ICAR–IARI, New Delhi.
- [Official bulletin index](https://creams.iari.res.in/?page_id=1123).
- Exact source: [Monitoring Paddy Residue Burning in India Using Satellite Remote Sensing During 2025, bulletin 77, 30-Nov-2025](https://creams.iari.res.in/Creams_website_bulletin/Fire_bulletin_2025/Fire_bulletin_2025r/77.RiceResidueFireBulletin_30Nov_2025_ICAR.pdf).
- Archive: `data/primary_sources/iari_paddy_bulletin_77_2025-11-30.pdf`.
- Extraction: one-based **PDF pages 25–27**, table “State-wise and date-wise number of paddy residue burning events detected in 2020, 2021, 2022, 2023, 2024 and 2025”, first panel (Punjab, Haryana, Uttar Pradesh). The Total row is on PDF page 27. Page references are PDF positions, not inferred printed page labels.
- Outputs: `iari_state_daily_fires.csv` (1,386 rows: 77 days × 6 years × 3 states) and `caqm_stubble_burning_annual_totals.csv` (18 rows; historical filename retained, actual reporting agency is IARI).
- Every output row carries `source_id`, `source_pdf_page`, and `source_row`; join `source_id` to the source manifest for the exact URL/hash. Geography is explicitly **whole state**, not NCR-only Uttar Pradesh. Year denotes the observed season, not the release year.
- The parser rejects missing dates, duplicate dates, malformed column counts, absent Total rows and any daily/seasonal mismatch. It parses the published numbers rather than emitting constants. There is no offline fallback that fabricates observations.

| Season | Punjab | Haryana | Uttar Pradesh (whole state) |
| --- | ---: | ---: | ---: |
| 2020 | 83,002 | 4,202 | 4,631 |
| 2021 | 71,304 | 6,987 | 4,242 |
| 2022 | 49,922 | 3,661 | 3,017 |
| 2023 | 36,663 | 2,303 | 3,996 |
| 2024 | 10,909 | 1,406 | 6,142 |
| 2025 | 5,114 | 662 | 7,290 |

These are detected crop-residue fire events under the bulletin's satellite methodology. They are not burned area, emission mass, smoke transport or a measured fraction of Delhi pollution. Cloud/overpass/detection limitations require consideration; do not derive causal source contributions from correlations alone.

No project dataset currently provides verified **district daily** observations. The bulletin's district seasonal tables cannot be allocated across dates to create them. Missing district observations are not zeros.

## 3. Historical source apportionment: IIT Kanpur / DPCC

- Issuer: IIT Kanpur, Mukesh Sharma and Onkar Dikshit; submitted to Delhi Department of Environment and DPCC. The report is not a current CPCB monitoring dataset.
- [Primary report on the principal investigator's IIT Kanpur website](https://home.iitk.ac.in/~mukesh/Publications/DPCC_2016_SA%20study%20IIT%20Kanpur%20report_Comprehensive%20Study%20on%20Air%20Pollution%20and%20Green%20House%20Gases%20%28GHGs%29%20in%20Delhi.pdf).
- Title: *Comprehensive Study on Air Pollution and Green House Gases (GHGs) in Delhi (Final Report: Air Pollution component)*. Repository labels it DPCC 2016; the cover has January 2016 and November 2015 text. Winter sampling occurred in 2013–2014, summer in 2014; site dates differ.
- Archive: `data/primary_sources/iitk_dpcc_delhi_report_2016.pdf`.
- Winter: **Table 4.20(b)**, Overall row, printed page **248**, PDF page **293**.
- Summer: **Table 4.24(b)**, Overall row, printed page **250**, PDF page **295**.
- Method: Chemical Mass Balance receptor modelling. Extract the nine percentage source contributions in their original order, retaining precision. The table title also contains a concentration unit parenthetical; the source-contribution columns are percentages, while its measured PM2.5 column is concentration and is not included in the output shares.
- Output: `iitk_dpcc_pm25_apportionment.csv`; 18 rows with source URL/hash linkage, PDF/printed pages, table and row locators. Winter shares sum to 100.00%; summer to 100.10% as published. Preserve that rounding discrepancy; do not normalize or invent a balancing category.

| Original category | Winter % | Summer % |
| --- | ---: | ---: |
| Secondary particles | 29.88 | 14.89 |
| Biomass burning | 25.84 | 12.16 |
| Industrial | 0.78 | 1.19 |
| Coal and fly ash | 4.79 | 25.95 |
| Construction material | 1.52 | 3.00 |
| Soil and road dust | 4.29 | 27.07 |
| Boiler | 0.01 | 0.11 |
| Solid waste burning | 7.75 | 7.23 |
| Vehicles | 25.14 | 8.50 |

The Overall statistic is from the report's six sampling sites and historical sampling periods. It is not a daily share or a spatially complete population-weighted Delhi estimate. Biomass burning is not exclusively Punjab/Haryana crop residue. Chemical marker and causal explanation fields from the old CSV were removed because they lacked row-specific evidence.

## Quarantine and acceptance

`data/quarantine/README.md` describes the rejected legacy inputs. Those files are excluded from ingestion and accepted loaders. The unrelated 2024/2025 PIB releases must never be cited as fire audits. The real 2023 PIB release (1981276) was published 30-Nov-2023, but the unified IARI bulletin now supplies the active fire data.

The machine-readable manifest pins evidence and explicitly records unresolved requirements. The verification report distinguishes integrity from milestone completion. Primary telemetry lineage, license applicability and the original district daily scope remain unresolved. No source authenticates a causal conclusion simply by being official.
