from __future__ import annotations

import json
import sys
import tempfile
import unittest
from contextlib import redirect_stdout
from io import StringIO
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from agentic_ready.audit import audit_target
from agentic_ready.cli import main


class SmokeTest(unittest.TestCase):
    def test_ready_fixture_passes_all_dimensions(self):
        report = audit_target(str(ROOT / "tests" / "fixtures" / "ready"))

        self.assertEqual(report.level, "Ready")
        self.assertEqual(report.score, 5)
        self.assertTrue(all(item.status == "pass" for item in report.dimensions))

    def test_not_ready_fixture_has_clear_drop_reasons(self):
        report = audit_target(str(ROOT / "tests" / "fixtures" / "not-ready"))

        self.assertEqual(report.level, "Not ready")
        self.assertLessEqual(report.score, 1)
        self.assertGreaterEqual(len(report.failed_or_partial), 4)

    def test_cli_json_and_threshold(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            output = Path(tmpdir) / "report.json"
            exit_code = main(
                [
                    str(ROOT / "tests" / "fixtures" / "ready"),
                    "--json",
                    "--output",
                    str(output),
                    "--fail-under",
                    "ready",
                ]
            )

            self.assertEqual(exit_code, 0)
            data = json.loads(output.read_text())
            self.assertEqual(data["level"], "Ready")

    def test_cli_threshold_failure(self):
        with redirect_stdout(StringIO()):
            exit_code = main(
                [
                    str(ROOT / "tests" / "fixtures" / "not-ready"),
                    "--fail-under",
                    "evaluable",
                ]
            )
        self.assertEqual(exit_code, 1)


if __name__ == "__main__":
    unittest.main()
