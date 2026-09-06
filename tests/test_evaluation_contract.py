import contextlib
import json
from pathlib import Path
import shlex
import subprocess
import sys
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]
HARNESS = ROOT / "tests/fixtures/evaluation_harness.py"


def make_workspace(directory):
    workspace = Path(directory)
    assets = {
        "prompts/prompt.json": {"id": "prompt", "variables": {"text": {"type": "string"}}, "template": "Uppercase {{text}}"},
        "evaluators/exact.json": {"id": "exact", "type": "deterministic", "metrics": ["exact_match_score"], "metric_definitions": {"exact_match_score": {"version": "1.0.0", "direction": "higher_is_better", "unit": "ratio"}}},
        "suites/demo.json": {"id": "demo", "name": "Demo", "prompt": "prompt", "datasets": ["examples"], "evaluators": ["exact"], "model_matrix": ["local:uppercase"], "trials": 1, "thresholds": {"exact_match_score": 0.0}},
        "harnesses/local.json": {"id": "deterministic-test-target", "type": "harness_adapter", "capabilities": ["run_suite"], "version": "1.0.0", "execution_mode": "measured", "entrypoint": shlex.join([sys.executable, str(HARNESS), "valid"])},
    }
    for relative, data in assets.items():
        path = workspace / "promptops" / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(data))
    dataset = workspace / "promptops/datasets/examples.jsonl"
    dataset.parent.mkdir()
    dataset.write_text(json.dumps({"case_id": "one", "inputs": {"text": "hello"}, "expected_outputs": {"text": "HELLO"}}) + "\n")
    return workspace, workspace / "promptops/harnesses/local.json"


class EvaluationExecutionTests(unittest.TestCase):
    def run_harness(self, variant="valid", model="local:uppercase", request_overrides=None, suite_overrides=None):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        directory = Path(temporary.name)
        workspace, _ = make_workspace(directory)
        suite_path = workspace / "promptops/suites/demo.json"
        suite = json.loads(suite_path.read_text())
        suite["thresholds"]["exact_match_score"] = 0.8
        suite.update(suite_overrides or {})
        suite_path.write_text(json.dumps(suite))
        from promptops.runtime.suite import build_request
        with contextlib.chdir(workspace):
            request = build_request("demo", [model])
        request.update(request_overrides or {})
        request_path = directory / "request.json"
        request_path.write_text(json.dumps(request))
        adapter = directory / "adapter.json"
        adapter.write_text(json.dumps({
            "id": "deterministic-test-target", "type": "harness_adapter", "capabilities": ["run_suite"], "version": "1.0.0", "execution_mode": "measured",
            "entrypoint": shlex.join([sys.executable, str(HARNESS), variant]),
        }))
        output = directory / "evidence"
        result = subprocess.run(
            [sys.executable, "-m", "promptops.runtime.runner", str(request_path), str(adapter), str(output)],
            cwd=ROOT, capture_output=True, text=True, timeout=15,
        )
        return result, output

    def test_invalid_request_is_rejected_before_the_harness_runs(self):
        for override in ({"thresholdz": {}}, {"cases": None}, {"trials": 0},
                         {"prompt_digest": "sha256:" + "0" * 64},
                         {"thresholds": {"exact_match_score": -1}},
                         {"expected_case_ids": ["invented"]}):
            with self.subTest(override=override):
                result, output = self.run_harness(request_overrides=override)
                self.assertNotEqual(result.returncode, 0)
                self.assertFalse((output / "run_manifest.json").exists())

    def test_zero_exit_does_not_make_empty_or_invalid_evidence_successful(self):
        for variant in ("empty-metrics", "empty-cases", "wrong-model", "failed-manifest", "fixture", "wrong-digest", "duplicate-case", "duplicate-trial", "score-drift", "request-tamper"):
            with self.subTest(variant=variant):
                result, _ = self.run_harness(variant)
                self.assertNotEqual(result.returncode, 0, result.stdout + result.stderr)
                self.assertNotIn("Success:", result.stdout)

    def test_cost_budget_needs_a_measurement_and_accepts_real_zero(self):
        for variant, expected in (("valid", False), ("zero-cost", True), ("invalid-cost", False)):
            result, output = self.run_harness(variant, suite_overrides={"budgets": {"cost_budget": 0}})
            self.assertEqual(result.returncode == 0, expected, result.stdout + result.stderr)

    def test_timeout_and_absent_policy_do_not_pass(self):
        result, output = self.run_harness("timeout", suite_overrides={"timeouts": {"run": 0.05}})
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("timed out", result.stderr)
        result, output = self.run_harness(suite_overrides={"thresholds": {}})
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(json.loads((output / "evaluation.json").read_text())["status"], "not_evaluated")

    def test_real_target_produces_a_durable_passing_decision(self):
        result, output = self.run_harness()
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        decision = json.loads((output / "evaluation.json").read_text())
        self.assertEqual(decision["status"], "pass")
        self.assertEqual(decision["metrics"], {"exact_match_score": 1.0})
        self.assertTrue((output / "run_request.json").is_file())

    def test_referenced_evidence_is_content_checked_on_readback(self):
        from promptops.runtime.gate import admit_run
        result, output = self.run_harness("raw-reference")
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        adapter = output.parent / "adapter.json"
        self.assertEqual(admit_run(output, adapter)["decision"]["status"], "pass")
        (output / "trace.txt").write_text("altered")
        with self.assertRaisesRegex(ValueError, "reference"):
            admit_run(output, adapter)

    def test_completed_execution_can_fail_its_quality_threshold(self):
        result, output = self.run_harness(model="local:lowercase")
        self.assertNotEqual(result.returncode, 0, result.stdout + result.stderr)
        decision = json.loads((output / "evaluation.json").read_text())
        self.assertEqual(decision["status"], "fail")
        self.assertEqual(decision["metrics"], {"exact_match_score": 0.0})

    def test_adapter_process_failure_is_not_reclassified_as_success(self):
        result, output = self.run_harness("process-failure")
        self.assertEqual(result.returncode, 7)
        self.assertFalse((output / "evaluation.json").exists())

    def test_reference_adapter_cannot_emit_measured_results_directly(self):
        with tempfile.TemporaryDirectory() as directory:
            request = Path(directory) / "request.json"
            request.write_text("{}")
            output = Path(directory) / "evidence"
            result = subprocess.run(
                [sys.executable, str(ROOT / "promptops/harnesses/reference-adapter/run.py"), str(request), str(output)],
                cwd=ROOT, capture_output=True, text=True, timeout=15,
            )
            self.assertNotEqual(result.returncode, 0)
            self.assertFalse((output / "scorecard.json").exists())


class SuiteExecutionTests(unittest.TestCase):
    def test_comparison_cannot_split_its_way_around_the_suite_cost_budget(self):
        from promptops.runtime.suite import evaluate_suite
        from promptops.runtime.compare import run_comparison
        with tempfile.TemporaryDirectory() as directory:
            workspace, adapter = make_workspace(directory)
            suite_path = workspace / "promptops/suites/demo.json"
            suite = json.loads(suite_path.read_text())
            suite["model_matrix"] = ["local:uppercase", "local:lowercase"]
            suite["budgets"] = {"cost_budget": 1}
            suite_path.write_text(json.dumps(suite))
            harness = workspace / "metered_target.py"
            harness.write_text(HARNESS.read_text().replace('"execution_mode": "measured"', '"total_cost": 0.75 * len(request["model_matrix"]), "execution_mode": "measured"'))
            config = json.loads(adapter.read_text())
            config["entrypoint"] = shlex.join([sys.executable, str(harness), "valid"])
            adapter.write_text(json.dumps(config))
            with contextlib.chdir(workspace):
                self.assertEqual(evaluate_suite("demo", adapter, workspace / "evaluation")["status"], "fail")
                with self.assertRaisesRegex(ValueError, "budget"):
                    run_comparison("demo", adapter_config=adapter, output_dir=workspace / "comparison")
            self.assertFalse((workspace / "comparison/comparison.json").exists())
            self.assertTrue((workspace / "comparison/model-1/evaluation.json").is_file())

    def test_explicit_adapter_version_is_not_replaced_with_a_runtime_default(self):
        from promptops.runtime.suite import evaluate_suite
        with tempfile.TemporaryDirectory() as directory:
            workspace, adapter = make_workspace(directory)
            config = json.loads(adapter.read_text())
            config["version"] = "2.0.0"
            adapter.write_text(json.dumps(config))
            harness = workspace / "v2_target.py"
            harness.write_text(HARNESS.read_text().replace('"harness_version": "1.0.0"', '"harness_version": "2.0.0"'))
            config["entrypoint"] = shlex.join([sys.executable, str(harness), "valid"])
            adapter.write_text(json.dumps(config))
            with contextlib.chdir(workspace):
                result = evaluate_suite("demo", adapter, workspace / "evidence")
            self.assertEqual(result["status"], "pass")
            request = json.loads((workspace / "evidence/run_request.json").read_text())
            self.assertEqual(request["harness_version"], "2.0.0")

    def test_shell_runner_accepts_complete_measured_evidence(self):
        with tempfile.TemporaryDirectory() as directory:
            workspace, adapter = make_workspace(directory)
            from promptops.runtime.suite import build_request
            with contextlib.chdir(workspace):
                data = build_request("demo")
            request = workspace / "request.json"
            request.write_text(json.dumps(data))
            result = subprocess.run(
                ["bash", str(ROOT / "promptops/runs/runner-shim.sh"), str(adapter), str(request), str(workspace / "evidence")],
                cwd=workspace, env={"PATH": "/usr/bin:/bin", "PYTHON": sys.executable}, capture_output=True, text=True, timeout=15,
            )
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertEqual(json.loads(result.stdout)["status"], "pass")

    def test_shell_runner_cannot_accept_a_manifest_only_harness(self):
        with tempfile.TemporaryDirectory() as directory:
            workspace, adapter = make_workspace(directory)
            harness = workspace / "manifest_only.py"
            harness.write_text("import sys\nfrom pathlib import Path\noutput = Path(sys.argv[2])\noutput.mkdir(parents=True, exist_ok=True)\n(output / 'run_manifest.json').write_text('{}')\n")
            config = json.loads(adapter.read_text())
            config["entrypoint"] = shlex.join([sys.executable, str(harness)])
            adapter.write_text(json.dumps(config))
            request = workspace / "request.json"
            request.write_text("{}")
            result = subprocess.run(
                ["bash", str(ROOT / "promptops/runs/runner-shim.sh"), str(adapter), str(request), str(workspace / "evidence")],
                cwd=workspace, env={"PATH": "/usr/bin:/bin", "PYTHON": sys.executable}, capture_output=True, text=True, timeout=15,
            )
            self.assertNotEqual(result.returncode, 0)
            self.assertFalse((workspace / "evidence/run_manifest.json").exists())

    def test_cli_evaluation_retains_resolved_inputs_and_measured_results(self):
        with tempfile.TemporaryDirectory() as directory:
            workspace, adapter = make_workspace(directory)
            output = workspace / "evidence"
            result = subprocess.run(
                [sys.executable, str(ROOT / "bin/apastra"), "eval", "demo", "--adapter", str(adapter), "--output-dir", str(output)],
                cwd=workspace, capture_output=True, text=True, timeout=15,
            )
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            decision = json.loads(result.stdout)
            self.assertEqual(decision["status"], "pass")
            request = json.loads((output / "run_request.json").read_text())
            self.assertEqual(request["expected_case_ids"], ["one"])
            self.assertEqual(request["cases"][0]["inputs"], {"text": "hello"})

    def test_comparison_retains_both_distinct_measurements_and_their_evidence(self):
        with tempfile.TemporaryDirectory() as directory:
            workspace, adapter = make_workspace(directory)
            result = subprocess.run(
                [sys.executable, str(ROOT / "bin/apastra"), "compare", "demo", "--adapter", str(adapter), "--models", "local:uppercase", "local:lowercase", "--output-dir", str(workspace / "comparison")],
                cwd=workspace, capture_output=True, text=True, timeout=15,
            )
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            comparison = json.loads(result.stdout)
            self.assertEqual(comparison["metrics"], {"local:uppercase": {"exact_match_score": 1.0}, "local:lowercase": {"exact_match_score": 0.0}})
            from promptops.runtime.suite import validate_asset
            validate_asset(comparison, "comparison-scorecard")
            for run in comparison["runs"].values():
                self.assertTrue((Path(run) / "cases.jsonl").is_file())

    def test_mcp_uses_explicit_adapter_and_never_auto_selects_the_reference(self):
        from promptops.runtime.mcp_server import run_evaluation

        with tempfile.TemporaryDirectory() as directory:
            workspace, adapter = make_workspace(directory)
            with contextlib.chdir(workspace):
                missing = json.loads(run_evaluation("demo"))
                self.assertEqual(missing["status"], "unsupported")
                actual = json.loads(run_evaluation("demo", adapter_config=str(adapter), output_dir=str(workspace / "evidence")))
                self.assertEqual(actual["status"], "pass", actual)


if __name__ == "__main__":
    unittest.main()
