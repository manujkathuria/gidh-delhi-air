"""Small contracts for discoverable investigations and serializable plans."""
from dataclasses import asdict, dataclass
from typing import Tuple


@dataclass(frozen=True)
class Investigation:
    id: str
    title: str
    question: str
    status: str


@dataclass(frozen=True)
class AnalysisPlan:
    investigation: Investigation
    parameters: dict
    inputs: Tuple[dict, ...]
    outputs: dict
    steps: Tuple[str, ...]
    pending_decisions: Tuple[str, ...]
    results_available: bool = False

    def to_dict(self) -> dict:
        return {'schema_version': 1, **asdict(self)}
