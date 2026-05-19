from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

Level = Literal["Ready", "Evaluable", "Discoverable", "Not ready"]
Status = Literal["pass", "partial", "fail"]


@dataclass(frozen=True)
class Evidence:
    label: str
    path: str


@dataclass(frozen=True)
class Dimension:
    key: str
    name: str
    status: Status
    evidence: tuple[Evidence, ...]
    drop_reason: str
    fix: str


@dataclass(frozen=True)
class Report:
    target: str
    level: Level
    score: int
    max_score: int
    dimensions: tuple[Dimension, ...]
    warnings: tuple[str, ...]

    @property
    def failed_or_partial(self) -> tuple[Dimension, ...]:
        return tuple(item for item in self.dimensions if item.status != "pass")
