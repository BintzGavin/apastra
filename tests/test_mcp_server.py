import contextlib
import json
from pathlib import Path
import tempfile
import unittest

from promptops.runtime.mcp_server import run_evaluation
from promptops.runtime.digest import compute_digest
from tests.test_evaluation_contract import make_workspace


class McpServerTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.workspace, self.adapter = make_workspace(temporary.name)
        self.enterContext(contextlib.chdir(self.workspace))

    def test_missing_suite_and_path_traversal_fail(self):
        for ref, reason in (("missing-suite", "suite_not_found"), ("../secret", "unsafe_ref")):
            with self.subTest(ref=ref):
                result = json.loads(run_evaluation(ref))
                self.assertEqual(result["status"], "error")
                self.assertEqual(result["reason"], reason)

    def test_asset_path_traversal_is_rejected_before_execution(self):
        path = self.workspace / "promptops/suites/demo.json"
        suite = json.loads(path.read_text())
        suite["datasets"] = ["../secret"]
        path.write_text(json.dumps(suite))
        result = json.loads(run_evaluation("demo", adapter_config=str(self.adapter)))
        self.assertEqual(result["reason"], "unsafe_ref")

    def test_digest_identity_is_semantic_and_historical_refs_are_not_mislabeled(self):
        output = self.workspace / "evidence"
        result = json.loads(run_evaluation("demo", adapter_config=str(self.adapter), output_dir=str(output)))
        self.assertEqual(result["status"], "pass", result)
        request = json.loads((output / "run_request.json").read_text())
        for name, path in (("prompt_digest", "prompts/prompt.json"), ("dataset_digest", "datasets/examples.jsonl"), ("evaluator_digest", "evaluators/exact.json")):
            self.assertEqual(request[name], compute_digest(self.workspace / "promptops" / path))
        historical = json.loads(run_evaluation("demo", revision_ref="HEAD~1", adapter_config=str(self.adapter)))
        self.assertEqual(historical["status"], "error")
        self.assertIn("Historical", historical["message"])

    def test_suite_id_and_directory_dataset_resolution(self):
        (self.workspace / "promptops/suites/demo.json").rename(self.workspace / "promptops/suites/different-name.json")
        dataset = self.workspace / "promptops/datasets/examples"
        dataset.mkdir()
        (dataset.parent / "examples.jsonl").rename(dataset / "dataset.jsonl")
        result = json.loads(run_evaluation("demo", adapter_config=str(self.adapter), output_dir=str(self.workspace / "evidence")))
        self.assertEqual(result["status"], "pass", result)
