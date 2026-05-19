from __future__ import annotations

import argparse
import sys
from pathlib import Path

from .audit import audit_target
from .render import render_json, render_text

LEVEL_ORDER = {
    "not-ready": 0,
    "discoverable": 1,
    "evaluable": 2,
    "ready": 3,
}


def main(argv: list[str] | None = None) -> int:
    argv = list(sys.argv[1:] if argv is None else argv)
    if argv and argv[0] == "audit":
        argv = argv[1:]
    parser = build_parser()
    args = parser.parse_args(argv)
    target = args.target
    if not target:
        parser.print_help(sys.stderr)
        return 2

    report = audit_target(target, timeout=args.timeout)
    rendered = render_json(report) if args.json else render_text(report)
    if args.output:
        Path(args.output).write_text(rendered + "\n", encoding="utf-8")
    else:
        print(rendered)

    if args.fail_under:
        required = LEVEL_ORDER[args.fail_under]
        actual = LEVEL_ORDER[report.level.lower().replace(" ", "-")]
        if actual < required:
            return 1
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="agentic-ready",
        description="Smoke-test whether agents can discover, evaluate, and use a B2B product.",
    )
    parser.add_argument("target", nargs="?", help="Path or URL to audit.")
    parser.add_argument("--json", action="store_true", help="Emit JSON instead of text.")
    parser.add_argument("--output", help="Write the report to a file.")
    parser.add_argument("--timeout", type=float, default=8.0, help="URL fetch timeout in seconds.")
    parser.add_argument(
        "--fail-under",
        choices=("discoverable", "evaluable", "ready"),
        help="Exit 1 when the result is below this level.",
    )

    return parser
