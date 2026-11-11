# Milestone 1 repair audit

Tracking: https://github.com/manujkathuria/gidh-delhi-air/issues/2

## Delivered corrections

1. Preserved unsupported inputs and incorrect PIB archives under `data/quarantine/`. Disabled synthetic district ingestion/loading and the misleading PIB constant-returning parser.
2. Downloaded the primary IARI bulletin and IIT Kanpur report; archived exact bytes with source URLs, retrieval timestamps and SHA-256 checksums. Rebuilds use these pinned local documents, not silently changing network responses.
3. Replaced daily fire fabrication with 1,386 actual **state daily** observations from IARI's retrospective 2020–2025 table. Extracted all 18 published Total cells independently and checked each against the 77 daily counts. Whole-state geography is explicit.
4. Replaced 15 rounded/grouped benchmark rows with 18 original IITK/DPCC shares from Tables 4.20(b)/4.24(b), Overall rows, preserving the report's categories, precision and historical scope. Removed unsupported chemical marker and causal interpretation fields.
5. Downloaded Kaggle version 1 and metadata; confirmed **all five** telemetry CSVs match its archive members byte for byte. No telemetry values or publisher metadata were modified. This verifies redistribution identity, not the unpublished upstream transformation chain.
6. Added evidence checks, source/observation integrity checks, coverage/missingness reporting, and regression tests. Loaders for derived tables compare against primary extraction. Default CLI exits nonzero for incomplete readiness, even when integrity passes.
7. Rewrote source documentation to remove unsupported instrument, saturation, outage and certification claims and to state geographic, temporal and attribution limitations.

## Annual fire corrections

Values below compare the quarantined CSV with the active IARI table. Unlisted cells were unchanged.

| State | Season | Old | Source-backed |
| --- | ---: | ---: | ---: |
| Punjab | 2020 | 76,590 | 83,002 |
| Haryana | 2020 | 5,000 | 4,202 |
| Uttar Pradesh | 2020 | 4,659 | 4,631 |
| Uttar Pradesh | 2021 | 3,383 | 4,242 |
| Uttar Pradesh | 2023 | 5,143 | 3,996 |
| Punjab | 2024 | 10,885 | 10,909 |
| Uttar Pradesh | 2024 | 5,769 | 6,142 |
| Uttar Pradesh | 2025 | 3,215 | 7,290 |

## Remaining acceptance gaps

- **Primary telemetry lineage:** no original government exports or upstream ETL/QC code. A byte match with Kaggle does not close this gap.
- **District daily scope:** the replacement is a state-level series. Real district daily bulletins must be acquired and parsed, or the project owner must explicitly revise that scope. No geographic/time allocation was invented.
- **License:** the full Kaggle description claims OGD Platform India terms, but applicability to the original exports and curated redistribution requires confirmation. The description and metadata are archived. Its linked upstream GitHub repository returned 404; no ETL code was obtained.

Integrity checks can pass while these gaps remain. The verifier deliberately cannot issue milestone sign-off under the current evidence policy. Any future acceptance implementation must be backed by newly verified evidence, not by deleting blocker text.

## Verification boundary

`docs/milestone1_verification.json` records the implemented checks, coverage and missingness. The report does not certify the accuracy of publisher observations, the physical cause of missingness, or the applicability of 2013–2014 apportionment shares to later pollution events. Satellite active fires do not themselves quantify transported smoke or Delhi source contributions.
