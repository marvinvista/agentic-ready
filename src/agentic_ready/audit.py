from __future__ import annotations

import re

from .loaders import load_target
from .models import Dimension, Evidence, Report
from .rules import DIMENSIONS


def audit_target(target: str, *, timeout: float = 8.0) -> Report:
    docs, warnings = load_target(target, timeout=timeout)
    dimensions = tuple(_score_dimension(definition, docs) for definition in DIMENSIONS)
    score = sum(1 for item in dimensions if item.status == "pass")
    return Report(
        target=target,
        level=_level(dimensions),
        score=score,
        max_score=len(dimensions),
        dimensions=dimensions,
        warnings=warnings,
    )


def _score_dimension(definition: dict, docs: dict[str, str]) -> Dimension:
    evidence = _find_evidence(definition["strong"], docs)
    labels = {item.label for item in evidence}
    if len(labels) >= 2:
        status = "pass"
    elif labels:
        status = "partial"
    else:
        status = "fail"

    return Dimension(
        key=definition["key"],
        name=definition["name"],
        status=status,
        evidence=tuple(evidence[:5]),
        drop_reason=definition["drop_reason"],
        fix=definition["fix"],
    )


def _find_evidence(patterns: tuple[tuple[str, str], ...], docs: dict[str, str]) -> list[Evidence]:
    evidence: list[Evidence] = []
    for label, pattern in patterns:
        compiled = re.compile(pattern, re.IGNORECASE | re.MULTILINE)
        for path, content in docs.items():
            haystack = f"{path}\n{content}"
            if compiled.search(haystack):
                evidence.append(Evidence(label=label, path=path))
                break
    return evidence


def _level(dimensions: tuple[Dimension, ...]) -> str:
    passes = sum(1 for item in dimensions if item.status == "pass")
    partials = sum(1 for item in dimensions if item.status == "partial")
    if passes == 5:
        return "Ready"
    if passes >= 3 and passes + partials >= 4:
        return "Evaluable"
    if passes + partials >= 2:
        return "Discoverable"
    return "Not ready"
