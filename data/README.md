# Shared research data

| Directory/file | Purpose | Editing rule |
| --- | --- | --- |
| `delhi_air_quality_monitoring_dataset/` | Five unchanged files from accepted Kaggle version 1 | Preserve original bytes; source checks compare them to the archive. |
| `primary_sources/` | Pinned PDFs, archive and publisher metadata | Preserve bytes; register new evidence and its hash in the manifest. |
| `indian_official_sources/` | Source-backed reference tables extracted from PDFs | Regenerate through the ingestion command. |
| `quarantine/` | Unsupported legacy inputs and their inventory | Keep excluded from analyses and public exports. |
| `processed/` | Future cleaned observations and intermediate results | Generated locally; ignored by Git. |
| `published/` | Reviewed, small JSON/CSV artifacts intended for public use | Version control only deliberate publication exports. |
| `source_manifest.json` | Evidence identity, hashes and known lineage gaps | Update with evidence, not assumptions. |

This structure preserves existing audited dataset locations while giving preprocessing and publication separate destinations. Nothing under `data/` is automatically exposed by the website. Public export is an explicit step.
