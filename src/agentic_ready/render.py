from __future__ import annotations

import json
from dataclasses import asdict

from .models import Report


def render_text(report: Report) -> str:
    lines: list[str] = [
        f"Agentic readiness: {report.level}",
        f"Target: {report.target}",
        f"Score: {report.score}/{report.max_score}",
        "",
    ]

    blockers = [item for item in report.dimensions if item.status != "pass"]
    if blockers:
        lines.append("Why agents drop you:")
        for index, item in enumerate(blockers, start=1):
            lines.append(f"{index}. {item.drop_reason}")
        lines.append("")
        lines.append("Next best fix:")
        lines.append(_next_fix(blockers))
    else:
        lines.append("Why agents keep you:")
        lines.append("1. The product is findable, callable, inspectable, priced, and has visible proof.")
        lines.append("")
        lines.append("Next best fix:")
        lines.append("Keep machine-readable docs, schemas, examples, pricing, and proof fresh as the product changes.")

    lines.append("")
    lines.append("Evidence:")
    for item in report.dimensions:
        if item.evidence:
            found = ", ".join(f"{hit.label} ({hit.path})" for hit in item.evidence)
        else:
            found = "none"
        lines.append(f"- {item.name}: {item.status} - {found}")

    if report.warnings:
        lines.append("")
        lines.append("Warnings:")
        for warning in report.warnings[:5]:
            lines.append(f"- {warning}")

    return "\n".join(lines)


def render_json(report: Report) -> str:
    return json.dumps(asdict(report), indent=2)


def _next_fix(blockers) -> str:
    priority = {"call": 0, "trust": 1, "buy": 2, "find": 3, "defend": 4}
    first = sorted(blockers, key=lambda item: priority.get(item.key, 99))[0]
    return first.fix
