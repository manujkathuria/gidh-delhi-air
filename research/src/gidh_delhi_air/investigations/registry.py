"""Explicit discovery: adding an investigation does not change the CLI."""
from dataclasses import dataclass
from typing import Callable, Optional, Tuple
from gidh_delhi_air.investigations.models import AnalysisPlan, Investigation
from gidh_delhi_air.investigations.clean_days import DEFINITION
from gidh_delhi_air.investigations.clean_days.analysis import plan_from_parameters
from gidh_delhi_air.paths import PATHS, ProjectPaths


@dataclass(frozen=True)
class Registration:
    definition: Investigation
    planner: Callable[[dict, ProjectPaths], AnalysisPlan]


# Explicit registration keeps imports predictable; no plugin system is needed.
INVESTIGATIONS = {DEFINITION.id: Registration(DEFINITION, plan_from_parameters)}


def list_investigations() -> Tuple[Investigation, ...]:
    return tuple(INVESTIGATIONS[key].definition for key in sorted(INVESTIGATIONS))


def plan_investigation(investigation_id: str, parameters: Optional[dict] = None,
                       paths: ProjectPaths = PATHS) -> AnalysisPlan:
    try:
        entry = INVESTIGATIONS[investigation_id]
    except KeyError as exc:
        raise ValueError(f'Unknown investigation: {investigation_id}') from exc
    plan = entry.planner({} if parameters is None else parameters, paths)
    if plan.investigation.id != investigation_id:
        raise ValueError('Registered planner returned a different investigation ID')
    return plan
