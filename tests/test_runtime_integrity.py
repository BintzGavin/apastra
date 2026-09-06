import contextlib
import io
import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from promptops.resolver.packaged import PackagedResolver
from promptops.runtime import cli, compare
from promptops.runtime.resolve import load_manifest
from promptops.resolver.chain import ResolverChain


class RuntimeIntegrityTests(unittest.TestCase):
    def test_signed_artifacts_cannot_claim_unsupported_verification(self):
        for signature in ("arbitrary-signature", "invalid", "", None):
            with self.subTest(signature=signature):
                with self.assertRaisesRegex(NotImplementedError, "verification is not supported"):
                    PackagedResolver().verify_signature({"metadata": {"signature": signature}})

    def test_unsigned_artifacts_are_not_reported_as_verified(self):
        self.assertFalse(PackagedResolver().verify_signature({"metadata": {}}))

    def test_missing_adapter_cannot_create_a_scorecard(self):
        with tempfile.TemporaryDirectory() as directory:
            with self.assertRaisesRegex(ValueError, "adapter"):
                compare.invoke_harness({"suite_id": "demo", "model_matrix": ["demo-model"]}, out_dir=directory)
            self.assertEqual(list(Path(directory).iterdir()), [])

    def test_comparison_does_not_invent_unmeasured_tradeoffs(self):
        result = compare.aggregate_scorecards("demo", {"model": {"normalized_metrics": {"exact_match_score": 0.7}}})
        self.assertEqual(result["comparison_tradeoffs"], {"cost": {}, "quality": {"model": 0.7}, "latency": {}})

    def test_unimplemented_analysis_commands_exit_without_a_report(self):
        for command in ("apastra-review", "apastra-optimize"):
            with self.subTest(command=command), tempfile.TemporaryDirectory() as directory:
                prompt = Path(directory) / "prompt.json"
                prompt.write_text(json.dumps({"id": "demo"}))
                output, errors = io.StringIO(), io.StringIO()
                with mock.patch.object(sys, "argv", ["apastra", command, str(prompt)]):
                    with contextlib.redirect_stdout(output), contextlib.redirect_stderr(errors):
                        with self.assertRaises(SystemExit) as raised:
                            cli.main()
                self.assertNotEqual(raised.exception.code, 0)
                self.assertEqual(output.getvalue(), "")
                self.assertIn("not implemented", errors.getvalue())

    def test_manifest_resolution_validates_without_a_node_process(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "manifest.json"
            path.write_text(json.dumps({"version": "1.0", "prompts": {"demo": {"id": "demo", "override": "prompt.json"}}}))
            with mock.patch("subprocess.run", side_effect=AssertionError("Node process must not run")):
                manifest = load_manifest(str(path))
                with mock.patch("promptops.resolver.chain.LocalResolver.resolve", return_value="hello"):
                    self.assertEqual(ResolverChain().resolve("demo", manifest), "hello")

    def test_invalid_manifest_is_rejected_before_resolving(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "manifest.json"
            path.write_text(json.dumps({"version": "1.0", "prompts": {"demo": {"override": "prompt.json"}}}))
            with mock.patch("subprocess.run", side_effect=AssertionError("Node process must not run")):
                with self.assertRaisesRegex(RuntimeError, "Manifest schema validation failed"):
                    ResolverChain().resolve("demo", load_manifest(str(path)))
