"""Validate the committed teaching assets by their actual protocol type."""

from pathlib import Path
import unittest

from promptops.runtime.digest import load_asset
from promptops.runtime.suite import build_request, validate_asset

ROOT = Path(__file__).resolve().parents[1]


class AssetInventoryTests(unittest.TestCase):
    def test_prompt_dataset_evaluator_suite_and_quick_eval_inventory(self):
        inventory = []
        for directory, kind in (("prompts", "prompt-spec"), ("datasets", "dataset-case"), ("evaluators", "evaluator"), ("suites", "suite"), ("evals", "quick-eval")):
            for path in sorted((ROOT / "promptops" / directory).rglob("*")):
                if path.suffix not in (".json", ".yaml", ".yml", ".jsonl"):
                    continue
                data = load_asset(path)
                selected = kind
                if directory == "prompts" and isinstance(data, dict) and "specs" in data:
                    selected = "prompt-package"
                elif directory == "datasets" and path.suffix != ".jsonl":
                    selected = "dataset-manifest"
                inventory.append((path, selected))
                with self.subTest(path=str(path.relative_to(ROOT)), kind=selected):
                    rows = data if path.suffix == ".jsonl" else [data]
                    self.assertTrue(rows, "Empty dataset cannot validate")
                    for row in rows:
                        validate_asset(row, selected)
        self.assertGreater(len(inventory), 20)

    def test_committed_suites_resolve_complete_input_snapshots(self):
        import contextlib
        with contextlib.chdir(ROOT):
            for path in sorted((ROOT / "promptops/suites").glob("*.yaml")):
                with self.subTest(suite=path.name):
                    request = build_request(load_asset(path)["id"])
                    self.assertTrue(request["cases"])
                    self.assertTrue(request["required_metrics"])
