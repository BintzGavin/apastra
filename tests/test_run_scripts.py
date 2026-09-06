import contextlib
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

from promptops.runtime.suite import build_request
from promptops.runtime.runner import run
from tests.test_evaluation_contract import ROOT, make_workspace


class RunScriptTests(unittest.TestCase):
    def test_shell_digest_matches_fixed_unicode_numeric_vector(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "asset.yaml"
            path.write_text("b: é\na: 1.0\n")
            result = subprocess.run(["bash", str(ROOT / "promptops/validators/compute-digest.sh"), str(path)], cwd=directory, env={"PATH": "/usr/bin:/bin", "PYTHON": sys.executable}, capture_output=True, text=True)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(result.stdout.strip(), "sha256:09ad9fd2fb648cb2f62141215828ea00a62c299db05d20aa9ade2f527a301cc6")

    def test_baseline_and_regression_wrappers_admit_complete_runs(self):
        with tempfile.TemporaryDirectory() as directory:
            workspace, adapter = make_workspace(directory)
            with contextlib.chdir(workspace):
                request = build_request("demo")
                self.assertEqual(run(request, adapter, workspace / "candidate")["status"], "pass")
                self.assertEqual(run(request, adapter, workspace / "baseline")["status"], "pass")
            policy = workspace / "policy.json"
            policy.write_text(json.dumps({"baseline": "prod", "rules": [{"metric": "exact_match_score", "floor": 0.8, "direction": "higher_is_better", "severity": "blocker"}]}))
            commands = [
                ["bash", str(ROOT / "promptops/runs/establish_baseline.sh"), "demo", "prod", str(workspace / "baseline"), str(adapter)],
                ["bash", str(ROOT / "promptops/runs/generate_regression_report.sh"), str(workspace / "candidate"), str(workspace / "baseline"), str(policy), "report", str(adapter)],
            ]
            for command in commands:
                result = subprocess.run(command, cwd=workspace, env={"PATH": "/usr/bin:/bin", "PYTHON": sys.executable}, capture_output=True, text=True)
                self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertTrue((workspace / "derived-index/baselines/demo-prod.json").is_file())
            report = json.loads((workspace / "derived-index/regressions/report.json").read_text())
            self.assertEqual(report["status"], "pass")
            self.assertNotIn("cost_delta", report)
