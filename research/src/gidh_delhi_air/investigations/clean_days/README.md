# Clean days — investigation 001

Stable code/export ID: `clean-days`. Editorial brief: `content/episodes/001-clean-days/brief.md` at the repository root.

- `__init__.py`: identity, question and current status.
- `config.py`: validated parameters, including year, station selection and target-day count.
- `analysis.py`: plan construction and, later, the investigation-specific counting/comparison workflow.

The plan explicitly marks completeness rules, benchmark registration and multi-station rules pending. It produces no data files or results. Implement common station/day preparation in `preprocessing/`; implement this investigation's counting and streak decisions here.

Once the workflow exists, add `charts.py` for episode figures and `export.py` for its public artifact. Shared chart/export helpers should be extracted when multiple investigations need them. Do not start separate Python projects or copy the data loaders into an episode.

Working results will use `data/processed/investigations/clean-days/`; reviewed public outputs will use `data/published/investigations/clean-days/`. A future export should contain its source hashes, analysis version, parameter/rule choices and coverage. Changing those choices should create a new identifiable analysis version.
