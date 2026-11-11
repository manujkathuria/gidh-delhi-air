"""One repository layout for source handling and every investigation."""
from dataclasses import dataclass
from pathlib import Path
import re
from typing import Optional


def find_project_root(start: Optional[Path] = None) -> Path:
    """Locate the workspace by its markers, independent of cwd or module depth."""
    start = (start if start is not None else Path(__file__)).resolve()
    directory = start if start.is_dir() else start.parent
    for candidate in (directory, *directory.parents):
        if ((candidate / 'research/pyproject.toml').is_file()
                and (candidate / 'package.json').is_file()):
            return candidate
    raise FileNotFoundError('Cannot locate the Delhi Air workspace: expected research/pyproject.toml '
                            'and package.json. Run from a source checkout.')


def validate_investigation_id(value: str) -> str:
    if not re.fullmatch(r'[a-z][a-z0-9]*(?:-[a-z0-9]+)*', value):
        raise ValueError('Investigation IDs must use lowercase words separated by hyphens')
    return value


@dataclass(frozen=True)
class ProjectPaths:
    root: Path

    def __post_init__(self) -> None:
        object.__setattr__(self, 'root', Path(self.root).resolve())

    @property
    def telemetry(self) -> Path:
        return self.root / 'data/delhi_air_quality_monitoring_dataset'

    @property
    def reference(self) -> Path:
        return self.root / 'data/indian_official_sources'

    @property
    def source_manifest(self) -> Path:
        return self.root / 'data/source_manifest.json'

    @property
    def shared_processed(self) -> Path:
        return self.root / 'data/processed/shared'

    def investigation_processed(self, investigation_id: str) -> Path:
        return self.root / 'data/processed/investigations' / validate_investigation_id(investigation_id)

    def investigation_published(self, investigation_id: str) -> Path:
        return self.root / 'data/published/investigations' / validate_investigation_id(investigation_id)


PROJECT_ROOT = find_project_root()
PATHS = ProjectPaths(PROJECT_ROOT)
