"""Given/When/Then checks for model-specific policy outcomes."""
import contextlib
import json
from pathlib import Path
import shlex
import sys
import subprocess
import tempfile
import unittest
from tests.test_evaluation_contract import HARNESS, ROOT, make_workspace


class ModelPolicySemanticsTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.workspace, self.adapter = make_workspace(temporary.name)
        self.models = ["local:uppercase", "local:lowercase"]
        self.suite_path = self.workspace / "promptops/suites/demo.json"
        self.suite = json.loads(self.suite_path.read_text())
        self.suite.update(model_matrix=self.models, thresholds={"exact_match_score": 0.5})
        self.save_suite()

    def save_suite(self):
        self.suite_path.write_text(json.dumps(self.suite))

    def test_given_threshold_failure_when_comparing_then_all_models_are_retained(self):
        from promptops.runtime.compare import run_comparison
        from promptops.runtime.gate import admit_run
        with contextlib.chdir(self.workspace):
            result = run_comparison("demo", list(reversed(self.models)), self.adapter, self.workspace / "comparison")
        self.assertEqual(result["status"], "fail")
        self.assertEqual(result["execution_status"], "completed")
        self.assertEqual(result["models"], list(reversed(self.models)))
        self.assertEqual(result["model_results"][self.models[0]]["status"], "pass")
        self.assertEqual(result["model_results"][self.models[1]]["status"], "fail")
        self.assertEqual(result["model_results"][self.models[1]]["failed_criteria"], ["exact_match_score"])
        self.assertEqual(json.loads((self.workspace / "comparison/comparison.json").read_text()), result)
        for model, directory in result["runs"].items():
            self.assertEqual(result["metrics"][model], admit_run(directory, self.adapter)["decision"]["metrics"])

    def test_given_no_thresholds_when_comparing_then_policy_is_not_evaluated(self):
        from promptops.runtime.compare import run_comparison
        self.suite["thresholds"] = {}
        self.save_suite()
        with contextlib.chdir(self.workspace):
            result = run_comparison("demo", adapter_config=self.adapter, output_dir=self.workspace / "comparison")
        self.assertEqual(result["status"], "not_evaluated")
        self.assertTrue(all(item["status"] == "not_evaluated" for item in result["model_results"].values()))
        self.assertTrue((self.workspace / "comparison/comparison.json").is_file())

    def test_given_pooled_threshold_pass_when_evaluating_then_failing_model_blocks(self):
        from promptops.runtime.suite import evaluate_suite
        from promptops.runtime.gate import admit_run
        with contextlib.chdir(self.workspace):
            result = evaluate_suite("demo", self.adapter, self.workspace / "evaluation")
        self.assertEqual(result["metrics"]["exact_match_score"], 0.5)
        self.assertEqual(result["status"], "fail")
        self.assertEqual(result["schema_version"], "3.0")
        self.assertEqual(result["model_results"][self.models[0]]["metrics"], {"exact_match_score": 1.0})
        self.assertEqual(result["model_results"][self.models[1]], {"metrics": {"exact_match_score": 0.0}, "status": "fail", "failed_criteria": ["exact_match_score"]})
        self.assertEqual(admit_run(self.workspace / "evaluation", self.adapter)["decision"]["status"], "fail")

    def test_given_execution_error_when_comparing_then_no_complete_report_is_written(self):
        from promptops.runtime.compare import run_comparison
        with contextlib.chdir(self.workspace), self.assertRaisesRegex(ValueError, "local:broken"):
            run_comparison("demo", [self.models[0], "local:broken"], self.adapter, self.workspace / "comparison")
        self.assertFalse((self.workspace / "comparison/comparison.json").exists())
        self.assertTrue((self.workspace / "comparison/model-1/evaluation.json").is_file())

    def produce_scores(self, name, scores):
        from promptops.runtime.suite import build_request
        from promptops.runtime.runner import run
        harness = self.workspace / "scores.py"
        harness.write_text(HARNESS.read_text().replace('metrics = {next(iter(definitions)): score}', 'score = request["prompt"].get("extensions", {}).get("model_scores", {}).get(model, score)\n            metrics = {next(iter(definitions)): score}'))
        config = json.loads(self.adapter.read_text())
        config["entrypoint"] = shlex.join([sys.executable, str(harness), "valid"])
        self.adapter.write_text(json.dumps(config))
        prompt_path = self.workspace / "promptops/prompts/prompt.json"
        prompt = json.loads(prompt_path.read_text())
        prompt["extensions"] = {"model_scores": dict(zip(self.models, scores))}
        prompt_path.write_text(json.dumps(prompt))
        with contextlib.chdir(self.workspace):
            result = run(build_request("demo"), self.adapter, self.workspace / name)
        return result, self.workspace / name

    def test_given_opposite_model_deltas_when_regressing_then_improvement_cannot_mask_failure(self):
        from promptops.runtime.gate import regression
        self.suite["thresholds"] = {"exact_match_score": 0.0}
        self.save_suite()
        _, baseline = self.produce_scores("baseline", [0.5, 0.5])
        _, candidate = self.produce_scores("candidate", [1.0, 0.0])
        for severity, expected in (("blocker", "fail"), ("warning", "warning")):
            with self.subTest(severity=severity):
                policy = {"baseline": "prod", "rules": [{"metric": "exact_match_score", "allowed_delta": 0.1, "direction": "higher_is_better", "severity": severity}]}
                report = regression(candidate, baseline, policy, self.adapter)
                self.assertEqual(report["evidence"][0]["delta"], 0.0)
                self.assertEqual(report["status"], expected)
                self.assertEqual(report["model_results"][self.models[0]]["status"], "pass")
                failed = report["model_results"][self.models[1]]
                self.assertEqual(failed["status"], expected)
                self.assertEqual(failed["evidence"][0]["candidate_value"], 0.0)
                self.assertEqual(failed["evidence"][0]["baseline_value"], 0.5)
                self.assertEqual(failed["evidence"][0]["status"], "fail")

    def test_given_model_decision_tampering_when_reading_back_then_admission_fails(self):
        from promptops.runtime.gate import admit_run
        _, directory = self.produce_scores("candidate", [1.0, 0.0])
        path = directory / "evaluation.json"
        decision = json.loads(path.read_text())
        decision["model_results"][self.models[1]]["status"] = "pass"
        path.write_text(json.dumps(decision))
        with self.assertRaisesRegex(ValueError, "Stored evaluation"):
            admit_run(directory, self.adapter)

    def test_given_lower_is_better_when_thresholding_then_each_model_uses_inclusive_boundary(self):
        from promptops.runtime.suite import evaluate_suite
        evaluator_path = self.workspace / "promptops/evaluators/exact.json"
        evaluator = json.loads(evaluator_path.read_text())
        evaluator["metric_definitions"]["exact_match_score"]["direction"] = "lower_is_better"
        evaluator_path.write_text(json.dumps(evaluator))
        with contextlib.chdir(self.workspace):
            result = evaluate_suite("demo", self.adapter, self.workspace / "evaluation")
        self.assertEqual(result["metrics"]["exact_match_score"], 0.5)
        self.assertEqual(result["status"], "fail")
        self.assertEqual(result["model_results"][self.models[0]]["status"], "fail")
        self.assertEqual(result["model_results"][self.models[1]]["status"], "pass")
        result, _ = self.produce_scores("boundary", [0.5, 0.5])
        self.assertEqual(result["status"], "pass")

    def test_given_multiple_cases_and_trials_when_scoring_then_models_use_all_measurements(self):
        self.suite["trials"] = 2
        self.save_suite()
        dataset = self.workspace / "promptops/datasets/examples.jsonl"
        second = {"case_id": "two", "inputs": {"text": "world"}, "expected_outputs": {"text": "world"}}
        dataset.write_text(dataset.read_text() + json.dumps(second) + "\n")
        from promptops.runtime.suite import evaluate_suite
        with contextlib.chdir(self.workspace):
            result = evaluate_suite("demo", self.adapter, self.workspace / "evaluation")
        self.assertEqual(result["status"], "pass")
        for item in result["model_results"].values():
            self.assertEqual(item["metrics"], {"exact_match_score": 0.5})
            self.assertEqual(item["status"], "pass")

    def test_given_complete_policy_outcomes_when_using_cli_then_nonpassing_reports_are_retained(self):
        for threshold, expected in ((0.5, "fail"), (None, "not_evaluated")):
            with self.subTest(expected=expected):
                self.suite["thresholds"] = {} if threshold is None else {"exact_match_score": threshold}
                self.save_suite()
                output = self.workspace / expected
                result = subprocess.run([sys.executable, str(ROOT / "bin/apastra"), "compare", "demo", "--adapter", str(self.adapter), "--output-dir", str(output)], cwd=self.workspace, capture_output=True, text=True, timeout=15)
                self.assertEqual(result.returncode, 2, result.stdout + result.stderr)
                report = json.loads(result.stdout)
                self.assertEqual(report["status"], expected)
                self.assertEqual(json.loads((output / "comparison.json").read_text()), report)

    def test_given_old_or_invalid_decision_when_reading_back_then_clear_rerun_error(self):
        from promptops.runtime.gate import admit_run
        _, directory = self.produce_scores("candidate", [1.0, 1.0])
        path = directory / "evaluation.json"
        stored = json.loads(path.read_text())
        stored.pop("schema_version")
        for legacy in (stored, []):
            with self.subTest(legacy=type(legacy).__name__):
                path.write_text(json.dumps(legacy))
                with self.assertRaisesRegex(ValueError, "rerun evaluation"):
                    admit_run(directory, self.adapter)

    def test_given_lower_metric_regression_when_pool_is_unchanged_then_model_failure_blocks(self):
        from promptops.runtime.gate import regression
        self.suite["thresholds"] = {"exact_match_score": 1.0}
        self.save_suite()
        path = self.workspace / "promptops/evaluators/exact.json"
        evaluator = json.loads(path.read_text())
        evaluator["metric_definitions"]["exact_match_score"]["direction"] = "lower_is_better"
        path.write_text(json.dumps(evaluator))
        _, baseline = self.produce_scores("baseline", [0.5, 0.5])
        _, candidate = self.produce_scores("candidate", [0.0, 1.0])
        for limit in ({"floor": 0.5}, {"allowed_delta": 0.1}):
            with self.subTest(limit=limit):
                policy = {"baseline": "prod", "rules": [{"metric": "exact_match_score", "direction": "lower_is_better", "severity": "blocker", **limit}]}
                report = regression(candidate, baseline, policy, self.adapter)
                self.assertEqual(report["status"], "fail")
                self.assertEqual(report["evidence"][0]["status"], "pass")
                self.assertEqual(report["model_results"][self.models[1]]["evidence"][0]["status"], "fail")
