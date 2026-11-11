# Delhi Air — research, stories and a website

**North star:** turn a question we care about into a story people want to finish watching.

This repository supports a YouTube research series and a React + TypeScript website where viewers can inspect the supporting methods, sources and aggregate results. The first investigation is **Can You Find 30 Clean Days in Delhi?** Its analysis is pending.

## Workspace

```text
apps/web/                 React + TypeScript website (Vite)
research/                 Python package, uv lockfile and research tests
  src/gidh_delhi_air/      Evidence verification, source ingestion and data loading
  tests/                  Research regression checks
content/
  episodes/001-clean-days/ First episode brief; scripts/storyboards will follow
scripts/                  Workspace utilities and publication sync
data/                    Shared datasets, source manifest and quarantined inputs
  processed/              Generated research intermediates (ignored)
  published/              Reviewed public JSON/CSV exports
docs/                    Provenance, methodology and verification reports
```

See [workspace architecture](docs/architecture.md), [research commands](research/README.md), [web setup](apps/web/README.md), and [episode brief](content/episodes/001-clean-days/brief.md).

## Setup and run

From the repository root, with Node 22.12+ and uv installed:

```bash
npm install
uv sync --project research --locked
npm run dev                 # Local website; prints its URL
npm run check               # TypeScript and frontend lint
npm run build               # Production web bundle, no deployment
npm run research:verify     # Implemented source/integrity checks
npm run research:test       # Python regression suite
npm run research:ingest     # Rebuild reference tables from pinned PDFs
npm run research:investigations -- list
npm run research:investigations -- plan clean-days
```

Python commands can also run without npm:

```bash
uv run --project research python -m gidh_delhi_air.verify --integrity-only
uv run --project research python -m unittest discover -s research/tests -v
```

`npm run research:readiness` retains the original milestone acceptance check and exits 1 while its gaps remain. `research:verify` exits 0 only when implemented integrity checks pass; evidence failure exits 2. This distinction is intentional.

## Research → public results → website/video

Python will write preprocessing intermediates to `data/processed/` and reviewed public results to `data/published/`. `npm run research:sync` copies only published JSON/CSV artifacts to the web app. Root dev/build commands run this step automatically. No raw datasets or quarantined files are exposed by that step.

The video charts and website should use the same analysis outputs. The initial starter shows source links and an investigation marked pending, with no fabricated counts or conclusions. Hosting, a backend/API and video rendering are future decisions.

## Current evidence

- **Accepted telemetry:** 162,096 CAAQMS rows and 57,946 AQI rows, seven stations. Five local CSVs match the pinned Kaggle version 1 archive byte for byte. The project accepts this redistribution as its telemetry input; original government exports and upstream QC remain unaudited.
- **Source-backed fire records:** 1,386 state daily rows and 18 seasonal totals, Punjab/Haryana/whole Uttar Pradesh, Sep 15–Nov 30, 2020–2025. Extracted from IARI bulletin 77 with reconciled totals.
- **Historical apportionment:** 18 PM2.5 shares from the IITK/DPCC report's original tables, based on 2013–2014 sampling. They do not establish current daily source contributions.
- **Excluded:** synthetic district daily records and other unsupported inputs remain quarantined. Actual district daily data and license applicability are unresolved.

CAAQMS coverage is year-round across seven stations for 2024–2025, with missing individual measurements. Only Dwarka covers 2023. Six stations extend to August 2026 with July absent; Dwarka ends in 2025. AQI covers 2025 only. Diwali 2026 is not covered.

[Source registry](docs/data_provenance_and_citations.md) · [Repair audit](docs/milestone1_repair_audit.md) · [Verification report](docs/milestone1_verification.json) · [Data layout](data/README.md)

Tracking: [lineage repairs #2](https://github.com/manujkathuria/gidh-delhi-air/issues/2), [workspace structure #3](https://github.com/manujkathuria/gidh-delhi-air/issues/3).
