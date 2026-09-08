"""User-visible provider workflow acceptance; real local harness processes."""
import contextlib
import json
from pathlib import Path
import tempfile
import time
import unittest

from tests.test_evaluation_contract import make_workspace


class WorkflowTests(unittest.TestCase):
    def setUp(self):
        from promptops.runtime.mcp_workflow import EvaluationWorkspace
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.workspace, self.adapter = make_workspace(temporary.name)
        self.service = EvaluationWorkspace(self.workspace, "test-workspace", self.adapter)
        self.addCleanup(self.service.close)

    def finish(self, **kwargs):
        started = self.service.start_evaluation("demo", **kwargs)
        self.assertIn("run_id", started, started)
        for _ in range(200):
            result = self.service.get_run(started["run_id"])
            if result["status"] not in ("queued", "running"):
                return result
            time.sleep(.02)
        self.fail("Run never reached a terminal state")

    def test_complete_candidate_baseline_and_inspectable_evidence(self):
        baseline = self.finish()
        candidate = self.finish()
        self.assertEqual(candidate["outcome"], "success", candidate)
        report = self.service.compare_runs(candidate["run_id"], baseline["run_id"])
        self.assertEqual(report["outcome"], "success", report)
        self.assertEqual(report["differences"][0]["delta"], 0)
        evidence = self.service.get_case(candidate["run_id"], "one", "local:uppercase", 1)
        self.assertEqual(evidence["case"]["output"], "HELLO")
        self.assertEqual(evidence["case"]["inputs"], {"text": "hello"})

    def test_changed_cases_and_config_are_inconclusive(self):
        baseline = self.finish()
        for field, value in (("trials", 2), ("thresholds", {"exact_match_score": .9}),
                             ("sampling_config", {"temperature": .5}), ("timeouts", {"run": 10})):
            path = self.workspace / "promptops/suites/demo.json"
            original = path.read_text()
            suite = json.loads(original)
            suite[field] = value
            path.write_text(json.dumps(suite))
            candidate = self.finish()
            report = self.service.compare_runs(candidate["run_id"], baseline["run_id"])
            self.assertEqual(report["outcome"], "inconclusive", (field, report))
            path.write_text(original)
        path = self.workspace / "promptops/datasets/examples.jsonl"
        path.write_text(path.read_text().replace("hello", "world"))
        candidate = self.finish()
        self.assertEqual(self.service.compare_runs(candidate["run_id"], baseline["run_id"])["outcome"], "inconclusive")

    def test_unsupported_invalid_and_unsafe_inputs_never_execute(self):
        from promptops.runtime.mcp_workflow import EvaluationWorkspace
        other = EvaluationWorkspace(self.workspace, "test-workspace")
        self.addCleanup(other.close)
        self.assertEqual(other.start_evaluation("demo")["reason"], "adapter_required")
        self.assertEqual(self.service.start_evaluation("demo", revision_ref="HEAD~1")["outcome"], "unsupported")
        self.assertEqual(self.service.start_evaluation("../private")["reason"], "unsafe_ref")
        self.assertEqual(self.service.get_run("../private")["reason"], "unsafe_ref")
        (self.workspace / "promptops/suites/demo.json").write_text("null")
        self.assertEqual(self.service.start_evaluation("demo")["outcome"], "evaluation_failed")

    def test_missing_or_modified_evidence_never_becomes_regression(self):
        baseline = self.finish()
        candidate = self.finish()
        directory = self.workspace / "promptops/runs/mcp" / candidate["run_id"]
        (directory / "cases.jsonl").unlink()
        self.assertEqual(self.service.compare_runs(candidate["run_id"], baseline["run_id"])["outcome"], "inconclusive")
        self.assertEqual(self.service.get_case(candidate["run_id"], "one", "local:uppercase", 1)["outcome"], "inconclusive")

    def test_workspace_and_output_symlinks_are_rejected(self):
        from promptops.runtime.mcp_workflow import EvaluationWorkspace
        with tempfile.TemporaryDirectory() as outside:
            with self.assertRaises(ValueError):
                EvaluationWorkspace(Path(outside), "bad")
            target = self.workspace / "promptops/runs/mcp"
            target.rmdir()
            target.symlink_to(outside, target_is_directory=True)
            result = self.service.start_evaluation("demo")
            self.service.close()
            self.assertEqual(result.get("reason"), "unsafe_ref")

    def test_restart_reports_interruption_and_keeps_completed_runs(self):
        from promptops.runtime.mcp_workflow import EvaluationWorkspace
        done = self.finish()
        path = self.workspace / "promptops/runs/mcp" / (done["run_id"] + ".json")
        record = json.loads(path.read_text())
        record["status"] = "running"
        path.write_text(json.dumps(record))
        self.service.close()
        resumed = EvaluationWorkspace(self.workspace, "test-workspace", self.adapter)
        self.addCleanup(resumed.close)
        self.assertEqual(resumed.get_run(done["run_id"])["reason"], "server_interrupted")

    def test_slow_run_reports_progress_busy_then_terminal_failure(self):
        config = json.loads(self.adapter.read_text())
        config["entrypoint"] = config["entrypoint"].removesuffix("valid") + "timeout"
        self.adapter.write_text(json.dumps(config))
        started = self.service.start_evaluation("demo")
        time.sleep(.05)
        progress = self.service.get_run(started["run_id"])
        self.assertEqual(progress["status"], "running")
        self.assertGreater(progress["elapsed_seconds"], 0)
        self.assertEqual(progress["total_trials"], 1)
        self.assertEqual(self.service.start_evaluation("demo")["reason"], "workspace_busy")
        self.service.close()
        self.assertEqual(self.service.get_run(started["run_id"])["outcome"], "success")

    def test_timeout_process_failure_and_missing_thresholds_have_distinct_reasons(self):
        original = self.adapter.read_text()
        for variant, reason in (("process-failure", "harness_failed"), ("timeout", "harness_timeout"), ("empty-cases", "invalid_evidence")):
            config = json.loads(original)
            config["entrypoint"] = config["entrypoint"].removesuffix("valid") + variant
            self.adapter.write_text(json.dumps(config))
            path = self.workspace / "promptops/suites/demo.json"
            suite = json.loads(path.read_text())
            suite["timeouts"] = {"run": .1 if variant == "timeout" else 10}
            path.write_text(json.dumps(suite))
            result = self.finish()
            self.assertEqual(result["outcome"], "evaluation_failed")
            self.assertEqual(result["reason"], reason)
        self.adapter.write_text(original)
        suite["thresholds"] = {}
        path.write_text(json.dumps(suite))
        result = self.finish()
        self.assertEqual(result["outcome"], "inconclusive")
        self.assertEqual(result["reason"], "no_thresholds")

    def test_case_inspection_bounds_metadata_and_marks_truncation(self):
        path = self.workspace / "promptops/datasets/examples.jsonl"
        case = json.loads(path.read_text())
        case["metadata"] = {"note": "evidence " * 1000}
        path.write_text(json.dumps(case) + "\n")
        run = self.finish()
        result = self.service.get_case(run["run_id"], "one", "local:uppercase", 1, max_chars=100)
        self.assertIn("metadata", result["truncated_fields"])
        self.assertLessEqual(len(result["case"]["metadata"]), 100)


class DemoTests(unittest.TestCase):
    def test_prompt_regression_and_fix_with_same_cases_and_model(self):
        import shutil
        from promptops.runtime.mcp_workflow import EvaluationWorkspace
        from tests.test_evaluation_contract import ROOT
        with tempfile.TemporaryDirectory() as directory:
            workspace = Path(directory) / "workspace"
            shutil.copytree(ROOT / "promptops/examples/kody-regression/workspace", workspace)
            service = EvaluationWorkspace(workspace, "demo", "promptops/harnesses/local.json")
            self.addCleanup(service.close)
            def execute():
                started = service.start_evaluation("assistant-smoke")
                self.assertIn("run_id", started, started)
                for _ in range(300):
                    result = service.get_run(started["run_id"])
                    if result["status"] not in ("queued", "running"):
                        return result
                    time.sleep(.02)
                self.fail("Demo run did not finish")
            baseline = execute()
            path = workspace / "promptops/prompts/assistant.json"
            original = path.read_text()
            path.write_text(original.replace("Uppercase", "Lowercase"))
            candidate = execute()
            self.assertEqual(candidate["outcome"], "evaluation_failed")
            report = service.compare_runs(candidate["run_id"], baseline["run_id"])
            self.assertEqual(report["outcome"], "regression", report)
            self.assertLess(report["differences"][0]["delta"], 0)
            self.assertGreater(report["total_changed_cases"], 0)
            reference = report["changed_cases"][0]["candidate_evidence"]["arguments"]
            case = service.get_case(**reference)["case"]
            self.assertNotEqual(case["output"], case["expected_outputs"]["text"])
            self.assertEqual(service.compare_runs(baseline["run_id"], candidate["run_id"])["outcome"], "inconclusive")
            path.write_text(original)
            fixed = execute()
            self.assertEqual(service.compare_runs(fixed["run_id"], baseline["run_id"])["outcome"], "success")
