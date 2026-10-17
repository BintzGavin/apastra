import contextlib
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

from tests.test_evaluation_contract import HARNESS, ROOT, make_workspace


class PortableBaselineTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.parent = Path(temporary.name)
        self.workspace, self.adapter = make_workspace(self.parent / "original")
        self.policy = {"baseline": "prod", "rules": [{"metric": "exact_match_score", "allowed_delta": 0, "direction": "higher_is_better", "severity": "blocker"}]}
        from promptops.runtime.runner import run
        from promptops.runtime.suite import build_request
        from promptops.runtime.gate import establish_baseline
        with contextlib.chdir(self.workspace):
            request = build_request("demo")
            run(request, self.adapter, self.workspace / "evidence/baseline")
            run(request, self.adapter, self.workspace / "evidence/candidate")
            record = establish_baseline("demo", "prod", self.workspace / "evidence/baseline", self.adapter)
        self.record = self.workspace / record["baseline_path"]

    def test_given_established_baseline_when_recorded_then_path_is_relative_to_record(self):
        record = json.loads(self.record.read_text())
        self.assertFalse(Path(record["run_path"]).is_absolute())
        self.assertEqual((self.record.parent / record["run_path"]).resolve(), (self.workspace / "evidence/baseline").resolve())

    def test_given_workspace_and_evidence_moved_when_regressing_then_no_rerun_is_required(self):
        from promptops.runtime.gate import regression
        moved = self.parent / "moved"
        record_relative = self.record.relative_to(self.workspace)
        adapter_relative = self.adapter.relative_to(self.workspace)
        shutil.move(self.workspace, moved)
        candidate = moved / "evidence/candidate"
        original_bytes = (candidate / "evaluation.json").read_bytes()
        report = regression(candidate, moved / record_relative, self.policy, moved / adapter_relative, expected_suite="demo")
        self.assertEqual(report["status"], "pass")
        self.assertEqual((candidate / "evaluation.json").read_bytes(), original_bytes)

    def test_given_baseline_record_when_using_cli_then_it_resolves_the_record(self):
        policy = self.workspace / "policy.json"
        policy.write_text(json.dumps(self.policy))
        result = subprocess.run([sys.executable, str(ROOT / "bin/apastra"), "gate", str(self.workspace / "evidence/candidate"), "--baseline", str(self.record), "--policy", str(policy), "--adapter", str(self.adapter)], cwd=self.workspace, capture_output=True, text=True, timeout=15)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertEqual(json.loads(result.stdout)["status"], "pass")

    def test_given_legacy_absolute_record_when_regressing_then_valid_v3_evidence_is_accepted(self):
        from promptops.runtime.gate import regression
        record = json.loads(self.record.read_text())
        record["run_path"] = str(self.workspace / "evidence/baseline")
        self.record.write_text(json.dumps(record))
        report = regression(self.workspace / "evidence/candidate", self.record, self.policy, self.adapter)
        self.assertEqual(report["status"], "pass")

    def test_given_tampered_record_when_regressing_then_reference_is_rejected(self):
        from promptops.runtime.gate import regression
        original = json.loads(self.record.read_text())
        for field, value, reason in (("run_digest", "sha256:" + "0" * 64, "digest"), ("suite_id", "wrong-suite", "suite"), ("run_path", "missing-evidence", "directory"), ("run_path", "../../evidence/candidate", "digest")):
            with self.subTest(field=field):
                self.record.write_text(json.dumps({**original, field: value}))
                with self.assertRaisesRegex(ValueError, reason):
                    regression(self.workspace / "evidence/candidate", self.record, self.policy, self.adapter)

    def test_given_pinned_adapter_and_workspace_move_when_admitting_then_paths_do_not_change_identity(self):
        import hashlib
        import shlex
        from unittest import mock
        from promptops.runtime.suite import build_request
        from promptops.runtime.runner import run
        from promptops.runtime.gate import establish_baseline, regression
        target = self.adapter.parent / "target.py"
        target.write_text(HARNESS.read_text())
        config = json.loads(self.adapter.read_text())
        config["entrypoint"] = shlex.join([sys.executable, str(target), "valid"])
        config["implementation"] = {"files": {"target.py": "sha256:" + hashlib.sha256(target.read_bytes()).hexdigest()}}
        self.adapter.write_text(json.dumps(config))
        with contextlib.chdir(self.workspace):
            request = build_request("demo")
            run(request, self.adapter, self.workspace / "evidence/pinned-baseline")
            run(request, self.adapter, self.workspace / "evidence/pinned-candidate")
            record = establish_baseline("demo", "pinned", self.workspace / "evidence/pinned-baseline", self.adapter)
        moved = self.parent / "moved"
        adapter_relative = self.adapter.relative_to(self.workspace)
        shutil.move(self.workspace, moved)
        with mock.patch("subprocess.run", side_effect=AssertionError("Admission must not rerun the harness")):
            report = regression(moved / "evidence/pinned-candidate", moved / record["baseline_path"], self.policy, moved / adapter_relative)
        self.assertEqual(report["status"], "pass")
