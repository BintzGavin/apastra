import contextlib
import json
from pathlib import Path
import subprocess
import tempfile
import unittest

from tests.test_evaluation_contract import make_workspace


class CiGateTests(unittest.TestCase):
    def test_execute_and_evidence_modes_bind_to_revision_and_workspace(self):
        from promptops.runtime.ci import ci_gate
        with tempfile.TemporaryDirectory() as directory:
            workspace, adapter = make_workspace(directory)
            for command in (["git", "init", "-q"], ["git", "add", "promptops"], ["git", "-c", "user.name=Test", "-c", "user.email=test@example.invalid", "-c", "commit.gpgsign=false", "commit", "-qm", "test inputs"]):
                subprocess.run(command, cwd=workspace, check=True, capture_output=True)
            revision = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=workspace, text=True).strip()
            output = workspace / "evidence"
            with contextlib.chdir(workspace):
                with self.assertRaises(ValueError):
                    ci_gate("demo", adapter, revision, "evidence", output)
                actual = ci_gate("demo", adapter, revision, "execute", output)
                self.assertEqual(actual["status"], "pass")
                self.assertEqual(ci_gate("demo", adapter, revision, "evidence", output)["status"], "pass")
                with self.assertRaisesRegex(ValueError, "revision"):
                    ci_gate("demo", adapter, "b" * 40, "evidence", output)
                prompt = workspace / "promptops/prompts/prompt.json"
                data = json.loads(prompt.read_text())
                data["template"] = "Changed {{text}}"
                prompt.write_text(json.dumps(data))
                with self.assertRaisesRegex(ValueError, "workspace"):
                    ci_gate("demo", adapter, revision, "evidence", output)

    def test_mode_and_regression_configuration_are_not_silently_ignored(self):
        from promptops.runtime.ci import ci_gate
        for options in (("advisory", None, None), ("execute", "baseline", None), ("evidence", None, "policy")):
            mode, baseline, policy = options
            with self.subTest(mode=mode), self.assertRaises(ValueError):
                ci_gate("demo", "missing", "a" * 40, mode, "missing", baseline, policy)
