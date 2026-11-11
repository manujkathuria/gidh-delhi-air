# Python research workspace

One Python project supports the whole series. Shared source/preparation code is reused; each investigation owns its question, parameters, comparisons and charts.

```text
src/gidh_delhi_air/
  paths.py                  Central workspace and output locations
  evidence.py               Source-manifest identity and checksum handling
  loader.py                 Shared accepted/verified input loaders
  verify.py                 Shared evidence and consistency checks
  ingest/                   Extraction of source-backed reference tables
  preprocessing/            Shared cleaning/aggregation ownership; implementation pending
  investigations/
    models.py               Small investigation/plan contracts
    registry.py             Explicit discovery and planner registration
    __main__.py             Generic list/plan CLI
    clean_days/
      config.py             Validated, immutable investigation parameters
      analysis.py           Read-only plan; counting/analysis implementation pending
      README.md             Episode-specific responsibilities
 tests/
   test_lineage.py           Existing source and integrity regression checks
   test_investigations.py    Plan/configuration, output isolation and CLI checks
```

No new Python project, duplicated dataset or separate dependency environment is needed for the next video. Keep editorial material in root `content/episodes/`, not in analysis code.

## Commands

From the repository root:

```bash
uv sync --project research --locked
npm run research:investigations -- list
npm run research:investigations -- plan clean-days
npm run research:investigations -- plan clean-days --set year=2024 --json
npm run research:verify
npm run research:test
npm run research:ingest
```

Equivalent Python invocation without npm:

```bash
uv run --project research --locked python -m gidh_delhi_air.investigations plan clean-days --json
uv run --project research --locked python -m gidh_delhi_air.verify --integrity-only
uv run --project research --locked python -m unittest discover -s research/tests -v
```

`plan` is read-only: it describes parameters, source hashes, destinations, steps and open decisions. It does not perform analysis, create directories or write publication results. `--config file.json` accepts investigation-specific parameters; repeatable `--set key=JSON` overrides individual values. Invalid/unknown options return a nonzero exit status. The first investigation currently supports 2024/2025 and stations 3–9 because other years do not cover all seven stations for the full calendar year.

The original `gidh-delhi-air` console entry and `python -m gidh_delhi_air` still run evidence verification. Default readiness exits 1 while the original acceptance gaps remain; `--integrity-only` exits 0 when implemented checks pass, and evidence failure exits 2. The project's acceptance of Kaggle is distinct from the archive's recorded redistributor identity.

## Shared preparation versus an investigation

Common timestamp/station normalization, completeness assessment and daily aggregation belong in `preprocessing/` as they are implemented. A video-specific date window, station-combination rule, threshold comparison, streak calculation and interpretation belong in that investigation. Extract common helpers when there is actual reuse rather than duplicating code or building a plugin framework.

Each investigation starts with a definition, a validated configuration and a planner; add executable analysis, `charts.py` and `export.py` when the actual calculations exist. New registrations plug into the list/plan CLI without adding investigation-specific dispatch logic. See [the extension guide](src/gidh_delhi_air/investigations/README.md).

## Data and publication boundaries

Use `ProjectPaths` instead of reconstructing repository paths or relying on the working directory. Root discovery uses source-checkout markers, not the availability of a dataset.

- Accepted telemetry and pinned source documents remain unchanged under root `data/`.
- Shared prepared tables go to `data/processed/shared/`.
- Private working tables and video figures go to `data/processed/investigations/<id>/`.
- Reviewed public JSON/CSV outputs go to `data/published/investigations/<id>/`.
- `npm run research:sync` copies those reviewed artifacts into the web app's generated public directory.

Video figures and website findings should come from the same identifiable analysis version and rules. Plans and editorial drafts are not public results. No preprocessing, benchmark counts or streak findings have been generated yet.

Tracking: workspace organization issue https://github.com/manujkathuria/gidh-delhi-air/issues/3
