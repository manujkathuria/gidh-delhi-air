# Shared preprocessing

This package is the home for preparation that multiple investigations need. It currently defines ownership only; it does not transform observations.

As the first analysis is implemented, add focused modules for timestamp/station normalization, measurement quality assessment, and daily aggregation with valid-hour counts. Functions should accept observations and explicit rules, return new tables, preserve input frames, and make unknown observations distinguishable from zeros.

Write shared intermediates under `ProjectPaths.shared_processed`. Keep benchmark comparisons, festival windows, station-combination decisions and streak counting with their investigation unless they become genuinely shared. Never put a video's conclusion into a common cleaning rule.
