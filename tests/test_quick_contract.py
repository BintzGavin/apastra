import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

from tests.test_evaluation_contract import ROOT, make_workspace


class QuickEvaluationTests(unittest.TestCase):
    def test_inline_assertions_have_real_pass_and_fail_outcomes(self):
        with tempfile.TemporaryDirectory() as directory:
            workspace, adapter = make_workspace(directory)
            quick = workspace / "quick ' quoted.json"
            quick.write_text(json.dumps({"id": "quick", "prompt": "Uppercase {{text}}", "cases": [{"case_id": "one", "inputs": {"text": "hello"}, "assert": [{"type": "equals", "value": "HELLO"}]}], "thresholds": {"pass_rate": 1}}))
            for model, expected in (("local:uppercase", "pass"), ("local:lowercase", "fail")):
                result = subprocess.run(["bash", str(ROOT / "promptops/runs/quick-eval.sh"), str(quick), "--adapter", str(adapter), "--models", model, "--output-dir", str(workspace / model.replace(":", "-"))], cwd=workspace, env={"PATH": "/usr/bin:/bin", "PYTHON": sys.executable}, capture_output=True, text=True)
                self.assertEqual(result.returncode, 0 if expected == "pass" else 2, result.stdout + result.stderr)
                self.assertEqual(json.loads(result.stdout)["status"], expected)
