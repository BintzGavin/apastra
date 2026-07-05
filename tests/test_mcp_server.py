import hashlib
import importlib
import json
import os
import sys
import tempfile
import types
import unittest
from pathlib import Path
from unittest import mock


class FakeFastMCP:
    def __init__(self, name):
        self.name = name

    def tool(self):
        def decorator(func):
            return func

        return decorator

    def run(self):
        return None


def import_mcp_server_with_fake_dependency():
    mcp_module = types.ModuleType("mcp")
    server_module = types.ModuleType("mcp.server")
    fastmcp_module = types.ModuleType("mcp.server.fastmcp")
    fastmcp_module.FastMCP = FakeFastMCP
    server_module.fastmcp = fastmcp_module
    mcp_module.server = server_module

    with mock.patch.dict(
        sys.modules,
        {
            "mcp": mcp_module,
            "mcp.server": server_module,
            "mcp.server.fastmcp": fastmcp_module,
        },
    ):
        return importlib.import_module("promptops.runtime.mcp_server")


def sha256_text(value):
    return "sha256:" + hashlib.sha256(value.encode("utf-8")).hexdigest()


class McpServerTests(unittest.TestCase):
    def setUp(self):
        self.mcp_server = import_mcp_server_with_fake_dependency()

    def test_run_evaluation_fails_before_execution_when_suite_is_missing(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "promptops" / "harnesses" / "reference-adapter").mkdir(
                parents=True
            )
            (root / "promptops" / "harnesses" / "reference-adapter" / "adapter.yaml").write_text(
                "entrypoint: python fake.py\n",
                encoding="utf-8",
            )

            previous = os.getcwd()
            os.chdir(root)
            try:
                result = json.loads(self.mcp_server.run_evaluation("missing-suite"))
            finally:
                os.chdir(previous)

        self.assertEqual(result["status"], "error")
        self.assertEqual(result["reason"], "suite_not_found")

    def test_run_evaluation_rejects_suite_id_path_traversal(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "promptops").mkdir()
            (root / "promptops" / "secret.yaml").write_text(
                "id: secret\nname: Secret\ndatasets: []\nevaluators: []\nmodel_matrix: []\n",
                encoding="utf-8",
            )

            previous = os.getcwd()
            os.chdir(root)
            try:
                result = json.loads(self.mcp_server.run_evaluation("../secret"))
            finally:
                os.chdir(previous)

        self.assertEqual(result["status"], "error")
        self.assertEqual(result["reason"], "unsafe_ref")

    def test_run_evaluation_rejects_asset_ref_path_traversal(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "promptops" / "suites").mkdir(parents=True)
            (root / "promptops" / "datasets").mkdir(parents=True)
            (root / "promptops" / "evaluators").mkdir(parents=True)
            (root / "promptops" / "harnesses" / "reference-adapter").mkdir(
                parents=True
            )
            (root / "promptops" / "secret.jsonl").write_text(
                '{"case_id":"secret"}\n',
                encoding="utf-8",
            )
            (root / "promptops" / "evaluators" / "demo-judge.yaml").write_text(
                "id: demo-judge\ntype: deterministic\n",
                encoding="utf-8",
            )
            (root / "promptops" / "suites" / "unsafe-suite.yaml").write_text(
                "\n".join(
                    [
                        "id: unsafe-suite",
                        "name: Unsafe Suite",
                        "datasets:",
                        "  - ../secret",
                        "evaluators:",
                        "  - demo-judge",
                        "model_matrix:",
                        "  - default",
                        "",
                    ]
                ),
                encoding="utf-8",
            )
            (
                root
                / "promptops"
                / "harnesses"
                / "reference-adapter"
                / "adapter.yaml"
            ).write_text("entrypoint: python fake.py\n", encoding="utf-8")

            previous = os.getcwd()
            os.chdir(root)
            try:
                with mock.patch.object(self.mcp_server.subprocess, "run") as run_mock:
                    result = json.loads(self.mcp_server.run_evaluation("unsafe-suite"))
            finally:
                os.chdir(previous)

        self.assertEqual(result["status"], "error")
        self.assertEqual(result["reason"], "unsafe_ref")
        run_mock.assert_not_called()

    def test_run_evaluation_uses_referenced_asset_digests(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "promptops" / "suites").mkdir(parents=True)
            (root / "promptops" / "prompts").mkdir(parents=True)
            (root / "promptops" / "datasets").mkdir(parents=True)
            (root / "promptops" / "evaluators").mkdir(parents=True)
            (root / "promptops" / "harnesses" / "reference-adapter").mkdir(
                parents=True
            )

            prompt_text = "id: demo-v1\ntemplate: 'Summarize {{text}}'\n"
            dataset_text = '{"case_id":"one","inputs":{"text":"hello"}}\n'
            evaluator_text = "id: demo-judge\ntype: deterministic\n"

            (root / "promptops" / "prompts" / "demo-v1.yaml").write_text(
                prompt_text,
                encoding="utf-8",
            )
            (root / "promptops" / "datasets" / "demo-smoke.jsonl").write_text(
                dataset_text,
                encoding="utf-8",
            )
            (root / "promptops" / "evaluators" / "demo-judge.yaml").write_text(
                evaluator_text,
                encoding="utf-8",
            )
            (root / "promptops" / "suites" / "demo-suite.yaml").write_text(
                "\n".join(
                    [
                        "id: demo-suite",
                        "name: Demo Suite",
                        "prompt: demo-v1",
                        "datasets:",
                        "  - demo-smoke",
                        "evaluators:",
                        "  - demo-judge",
                        "model_matrix:",
                        "  - default",
                        "",
                    ]
                ),
                encoding="utf-8",
            )
            (root / "promptops" / "harnesses" / "reference-adapter" / "adapter.yaml").write_text(
                "entrypoint: python fake.py\n",
                encoding="utf-8",
            )

            captured_request = {}

            def fake_run(cmd, capture_output, text):
                request_path = Path(cmd[-3])
                output_dir = Path(cmd[-1])
                captured_request.update(json.loads(request_path.read_text()))
                output_dir.mkdir(parents=True, exist_ok=True)
                (output_dir / "scorecard.json").write_text(
                    json.dumps({"suite_id": "demo-suite", "normalized_metrics": {}}),
                    encoding="utf-8",
                )
                return types.SimpleNamespace(returncode=0, stdout="", stderr="")

            previous = os.getcwd()
            os.chdir(root)
            try:
                with mock.patch.object(self.mcp_server.subprocess, "run", fake_run):
                    result = json.loads(
                        self.mcp_server.run_evaluation("demo-suite", "HEAD")
                    )
            finally:
                os.chdir(previous)

        self.assertEqual(result["status"], "success")
        self.assertEqual(captured_request["prompt_digest"], sha256_text(prompt_text))
        self.assertEqual(captured_request["dataset_digest"], sha256_text(dataset_text))
        self.assertEqual(
            captured_request["evaluator_digest"],
            sha256_text(evaluator_text),
        )
        self.assertEqual(captured_request["evaluator_refs"], ["demo-judge"])

    def test_run_evaluation_resolves_suite_id_and_directory_assets(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "promptops" / "suites").mkdir(parents=True)
            (root / "promptops" / "datasets" / "test-dataset").mkdir(parents=True)
            (root / "promptops" / "evaluators").mkdir(parents=True)
            (root / "promptops" / "harnesses" / "reference-adapter").mkdir(
                parents=True
            )

            dataset_text = '{"case_id":"case-1","inputs":{"text":"hello"}}\n'
            evaluator_text = "id: exact-match-v1\ntype: deterministic\n"

            (root / "promptops" / "suites" / "test-suite.yaml").write_text(
                "\n".join(
                    [
                        "id: test-suite-v1",
                        "name: Test Suite",
                        "datasets:",
                        "  - test-dataset",
                        "evaluators:",
                        "  - exact-match-v1",
                        "model_matrix:",
                        "  - default",
                        "",
                    ]
                ),
                encoding="utf-8",
            )
            (
                root
                / "promptops"
                / "datasets"
                / "test-dataset"
                / "dataset.jsonl"
            ).write_text(dataset_text, encoding="utf-8")
            (root / "promptops" / "evaluators" / "exact-match.yaml").write_text(
                evaluator_text,
                encoding="utf-8",
            )
            (
                root
                / "promptops"
                / "harnesses"
                / "reference-adapter"
                / "adapter.yaml"
            ).write_text("entrypoint: python fake.py\n", encoding="utf-8")

            captured_request = {}

            def fake_run(cmd, capture_output, text):
                request_path = Path(cmd[-3])
                output_dir = Path(cmd[-1])
                captured_request.update(json.loads(request_path.read_text()))
                output_dir.mkdir(parents=True, exist_ok=True)
                (output_dir / "scorecard.json").write_text(
                    json.dumps({"suite_id": "test-suite-v1", "normalized_metrics": {}}),
                    encoding="utf-8",
                )
                return types.SimpleNamespace(returncode=0, stdout="", stderr="")

            previous = os.getcwd()
            os.chdir(root)
            try:
                with mock.patch.object(self.mcp_server.subprocess, "run", fake_run):
                    result = json.loads(self.mcp_server.run_evaluation("test-suite-v1"))
            finally:
                os.chdir(previous)

        self.assertEqual(result["status"], "success")
        self.assertEqual(captured_request["dataset_digest"], sha256_text(dataset_text))
        self.assertEqual(
            captured_request["evaluator_digest"],
            sha256_text(evaluator_text),
        )


if __name__ == "__main__":
    unittest.main()
