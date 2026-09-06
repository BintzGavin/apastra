import contextlib
from copy import deepcopy
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

from tests.test_evaluation_contract import ROOT, make_workspace


class GateContractTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.workspace, self.adapter = make_workspace(temporary.name)

    def produce(self, name="candidate", score=1):
        from promptops.runtime.runner import run
        from promptops.runtime.suite import build_request
        with contextlib.chdir(self.workspace):
            request = build_request("demo", ["local:uppercase" if score else "local:lowercase"])
            request["source_revision"] = "a" * 40
            output = self.workspace / name
            result = run(request, self.adapter, output)
        self.assertEqual(result["status"], "pass")
        return output

    def test_legacy_scorecard_only_and_empty_policy_cannot_pass(self):
        candidate = self.workspace / "candidate.json"
        candidate.write_text(json.dumps({"normalized_metrics": {"accuracy": 1}}))
        policy = self.workspace / "policy.json"
        policy.write_text(json.dumps({"baseline": "prod", "rules": []}))
        output = self.workspace / "report.json"
        result = subprocess.run([sys.executable, str(ROOT / "promptops/runs/compare.py"), str(candidate), str(candidate), str(policy), str(output)], capture_output=True, text=True)
        self.assertNotEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertFalse(output.exists())

    def test_stored_evidence_checks_producer_revision_and_content(self):
        from promptops.runtime.gate import admit_run
        output = self.produce()
        result = admit_run(output, self.adapter, expected_revision="a" * 40)
        self.assertEqual(result["decision"]["status"], "pass")
        with self.assertRaisesRegex(ValueError, "revision"):
            admit_run(output, self.adapter, expected_revision="b" * 40)
        adapter_data = json.loads(self.adapter.read_text())
        adapter_data["id"] = "unapproved"
        self.adapter.write_text(json.dumps(adapter_data))
        with self.assertRaisesRegex(ValueError, "producer"):
            admit_run(output, self.adapter)
        adapter_data["id"] = "deterministic-test-target"
        self.adapter.write_text(json.dumps(adapter_data))
        scorecard = output / "scorecard.json"
        data = json.loads(scorecard.read_text())
        data["normalized_metrics"]["exact_match_score"] = 0.2
        scorecard.write_text(json.dumps(data))
        with self.assertRaises(ValueError):
            admit_run(output, self.adapter)

    def test_policy_is_nonempty_typed_and_cannot_waive_flakes(self):
        from promptops.runtime.gate import evaluate_policy
        definitions = {"accuracy": {"unit": "ratio", "version": "1", "direction": "higher_is_better"}}
        candidate = {"normalized_metrics": {"accuracy": 0.5}, "metric_definitions": definitions, "flake_rates": {"accuracy": 1}}
        baseline = {"normalized_metrics": {"accuracy": 1}, "metric_definitions": definitions}
        policy = {"baseline": "prod", "rules": [{"metric": "accuracy", "floor": 0.8, "direction": "higher_is_better", "severity": "blocker"}]}
        self.assertEqual(evaluate_policy(candidate, baseline, policy)["status"], "fail")
        for rule in ({}, {"direction": "unknown"}, {"allowed_delta": -1}, {"severity": "ignore"}):
            invalid = deepcopy(policy)
            invalid["rules"] = [] if not rule else [{**policy["rules"][0], **rule}]
            with self.subTest(rule=rule), self.assertRaises(ValueError):
                evaluate_policy(candidate, baseline, invalid)
        candidate["metric_definitions"] = deepcopy(definitions)
        candidate["metric_definitions"]["accuracy"]["unit"] = "percent"
        with self.assertRaises(ValueError):
            evaluate_policy(candidate, baseline, policy)

    def test_inclusive_higher_and_lower_boundaries(self):
        from promptops.runtime.gate import evaluate_policy
        for direction, baseline_value, boundary, outside in (("higher_is_better", 1, 0.8, 0.799), ("lower_is_better", 1, 1.2, 1.201)):
            definitions = {"metric": {"version": "1", "unit": "ratio", "direction": direction}}
            baseline = {"normalized_metrics": {"metric": baseline_value}, "metric_definitions": definitions}
            policy = {"baseline": "prod", "rules": [{"metric": "metric", "allowed_delta": 0.2, "direction": direction, "severity": "blocker"}]}
            for value, expected in ((boundary, "pass"), (outside, "fail")):
                candidate = {"normalized_metrics": {"metric": value}, "metric_definitions": definitions}
                self.assertEqual(evaluate_policy(candidate, baseline, policy)["status"], expected)

    def test_baseline_requires_resolved_pass_and_never_overwrites(self):
        from promptops.runtime.gate import establish_baseline
        output = self.produce()
        with contextlib.chdir(self.workspace):
            with self.assertRaises(ValueError):
                establish_baseline("demo", "prod", "sha256:" + "0" * 64, self.adapter)
            record = establish_baseline("demo", "prod", output, self.adapter)
            path = self.workspace / record["baseline_path"]
            original = path.read_bytes()
            with self.assertRaises(FileExistsError):
                establish_baseline("demo", "prod", output, self.adapter)
            self.assertEqual(path.read_bytes(), original)
