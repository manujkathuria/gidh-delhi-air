# Workspace architecture

## Responsibilities

- `research/` is the Python/uv project. It owns evidence validation, ingestion and future preprocessing/analysis. Its `.python-version` preserves the original Python 3.9 pin.
- `apps/web/` is an npm workspace with React, TypeScript and Vite. It presents the research and episode material. It does not own scientific calculations.
- `content/` holds episode briefs, future findings notes, scripts and storyboards. Episode IDs remain stable across public exports, chart assets and web pages.
- `data/` remains shared, outside the public website. Existing evidence and telemetry paths are preserved to avoid changing audited files or their hashes.
- `docs/` holds research provenance and engineering conventions. `scripts/` contains workspace utilities.

## Publication boundary

Raw observations and official source documents feed Python. Python writes intermediates to `data/processed/`. Reviewed small JSON/CSV outputs go to `data/published/`. A Node sync step stages then replaces only `apps/web/public/research/`, ignoring other file types and rejecting symbolic links. The generated copy is ignored by Git. It is rebuilt before root web dev/build commands.

Only deliberately published aggregate exports should enter the publication directory; the sync utility cannot determine whether a file is scientifically valid or suitable for publication. It does not grant a new license. The source registry and remaining license questions still apply.

Future web charts and video chart renders should consume the same episode output, retaining source IDs, analysis versions, missingness rules and benchmark definitions. No production results are present yet.

## Local lifecycle

Research can run independently with `uv run --project research …`. Frontend setup uses the root `package-lock.json` and npm workspaces; use root `npm ci` on repeat installations. `npm run check` checks frontend types and lint. `npm run research:test` runs the existing research tests. `npm run build` produces `apps/web/dist/` without deploying it.

The current website is a starter page, not a finished research publication. No server, database, authentication or hosting dependency is required for this stage. Those can be introduced if future product requirements justify them.

## Migration notes

The former root `src/`, `tests/`, `pyproject.toml`, `uv.lock` and `.python-version` now live under `research/`. Python resolves the shared repository root from its package location. Existing manifest paths, source bytes, quarantine inventory and legacy compatibility APIs retain their meaning. Replace old `uv run python src/main.py` invocations with `uv run --project research python -m gidh_delhi_air.verify`.

Tracking: https://github.com/manujkathuria/gidh-delhi-air/issues/3

## Python investigation structure

The Python workspace now has shared `paths.py`, source/evidence/loading/verification modules, an `ingest/` package, a shared `preprocessing/` namespace and separately registered `investigations/`. Existing source APIs remain available. Source bytes and dataset locations were not changed.

A small `Investigation` definition, validated local configuration and read-only `AnalysisPlan` describe each question. The CLI lists investigations and inspects their inputs, destinations and pending decisions. `clean_days/` is the first registered investigation; it contains no computed conclusions. Additional questions register their own planner without changing CLI dispatch. There is no task scheduler, plugin discovery, database or caching framework.

Use `data/processed/shared/` for common prepared observations and `data/processed/investigations/<id>/` for a question's working outputs. Only reviewed results enter `data/published/investigations/<id>/`. Episode numbers remain editorial identifiers; descriptive stable code IDs such as `clean-days` connect the analysis to its editorial brief. Shared preparation may be reused; one investigation should not depend on another investigation's private analysis code.

The next implementation is shared daily preparation and completeness assessment, followed by clean-days benchmark comparisons and streak counting. Those scientific rules are still pending. See `research/README.md` for commands and the investigation extension guide.
