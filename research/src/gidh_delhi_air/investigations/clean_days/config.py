"""Parameters for the first investigation; no implicit scientific thresholds."""
from dataclasses import dataclass
from typing import Tuple


@dataclass(frozen=True)
class CleanDaysConfig:
    year: int = 2025
    target_days: int = 30
    station_ids: Tuple[int, ...] = (3, 4, 5, 6, 7, 8, 9)

    def __post_init__(self) -> None:
        # These are the complete calendar years currently represented at all seven stations.
        if type(self.year) is not int or self.year not in (2024, 2025):
            raise ValueError('Clean-days planning currently supports 2024 or 2025; other years have partial station coverage')
        if type(self.target_days) is not int or not 1 <= self.target_days <= (366 if self.year == 2024 else 365):
            raise ValueError('target_days must fit within the selected calendar year')
        if (not isinstance(self.station_ids, (list, tuple)) or not self.station_ids
                or any(type(station) is not int for station in self.station_ids)
                or len(set(self.station_ids)) != len(self.station_ids)
                or not set(self.station_ids).issubset({3, 4, 5, 6, 7, 8, 9})):
            raise ValueError('station_ids must be a nonempty, unique selection from stations 3–9')
        object.__setattr__(self, 'station_ids', tuple(self.station_ids))
