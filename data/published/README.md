# Public research exports

Only place intentionally public, reviewed JSON or CSV files here. `npm run research:sync` copies these file types to `apps/web/public/research/` before web development/build. Raw datasets, archives, quarantined inputs and documents are not copied.

Each future episode export should identify its schema version, analysis version/commit, study period, stations, completeness rule, pollutant and units, benchmark sources, and finding/source references. Missing or uncalculated findings must remain absent or explicitly null; do not publish placeholder counts as results.

Keep downloadable source citations as official URLs. The website and video chart exports should use the same computed results.
