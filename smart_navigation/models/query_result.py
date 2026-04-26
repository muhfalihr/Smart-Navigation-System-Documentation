"""Domain models for navigation result."""

from dataclasses import dataclass


@dataclass
class QueryResult:
    start: str
    end: str
    path: list[str]
    total_distance: float = 0.0
    total_time: float = 0.0

    @property
    def distance(self) -> float:
        return self.total_distance
