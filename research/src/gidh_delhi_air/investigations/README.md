# Investigations

Each investigation owns its question, validated parameters, analysis and eventual charts/public exports. All investigations reuse shared source loading, evidence checks and preprocessing.

## Add an investigation

1. Create a package with a descriptive Python name, e.g. `diwali/`.
2. Define a stable hyphenated ID, title, question and honest status in an `Investigation` record.
3. Define a small frozen configuration dataclass and reject invalid/unknown parameter combinations.
4. Add a planner accepting `(parameters: dict, paths: ProjectPaths)` and returning an `AnalysisPlan` with the inputs, destinations and unresolved methodology decisions. Planning must not write outputs or manufacture findings.
5. Register the definition/planner in `registry.py`. The generic list/plan CLI needs no investigation-specific flags or dispatch changes.
6. Add tests for the new investigation's parameters and scientific rules as those rules are implemented. Use synthetic fixtures only for tests, never as research observations.
7. Keep editorial planning in `content/episodes/<episode-id>/` and cross-link it to the stable code ID. Keep computation in the Python package.

Use `ProjectPaths` for all data locations. Source folders remain read-only. Working outputs and published artifacts are separated by investigation ID. Investigations do not import another investigation's private analysis; move genuinely reusable preparation into `preprocessing/` instead.

## Current CLI

From the repository root:

```bash
npm run research:investigations -- list
npm run research:investigations -- plan clean-days
npm run research:investigations -- plan clean-days --set year=2024 --json
```

Only listing and read-only planning exist today. Add execution commands when the actual workflows and their rule tests exist; do not let a successful plan look like completed analysis.
