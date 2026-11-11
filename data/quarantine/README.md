# Rejected legacy inputs — not empirical analysis inputs

These files preserve the pre-repair state. They are not ingested or accepted as verified official observations. `inventory.json` pins their original bytes. Git history retains the original generation code.

| File | Reason |
| --- | --- |
| `iari_district_daily_stubble_fires.csv` | Synthetic Gaussian seasonal curve × assumed district weights × hard-coded annual totals. Falsely labelled as IARI observations; sums do not reconcile. |
| `iari_daily_stubble_fires.csv` | Earlier daily series without specific bulletin IDs, raw evidence or a reproducible extraction path. Not accepted as observed data. |
| `caqm_stubble_burning_annual_totals.csv` | Old constants include incorrect values and unsupported references. Replaced in the active directory by extraction from IARI bulletin 77. |
| `cpcb_iitk_source_apportionment.csv` | Rounded/grouped shares with unsupported marker/causal annotations. Replaced by original table categories and precision from the IITK report. |
| `pib_release_2023_PRID_1981276.html` | Real fire-related release; old metadata misdated it and some generated values contradicted its text. Superseded by the unified IARI source; this file is retained as legacy evidence, not rejected as inauthentic. |
| `pib_release_2024_PRID_2078652.html` | Unrelated Prime Minister's Office release about enthusiasm for Indian history/culture, dated 28-Nov-2024. |
| `pib_release_2025_PRID_2196420.html` | Unrelated Prime Minister's Office release about the Raipur DGP/IGP conference, dated 29-Nov-2025. |

Do not move these files into `indian_official_sources/` or use their zeros as missing-data replacements. Actual district daily records are still required for the original district-level scope.
