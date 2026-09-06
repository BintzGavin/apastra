import contextlib
import io
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest import mock

from promptops.resolver.packaged import PackagedResolver
from promptops.runtime.resolve import ManifestWrapper
from promptops.resolver.chain import ResolverChain
from promptops.runtime.digest import compute_digest_from_dict

ROOT = Path(__file__).resolve().parents[1]


class CapabilityTests(unittest.TestCase):
    def test_cached_inline_package_resolves_offline_and_checks_its_digest(self):
        package = {"id": "package", "specs": [{"id": "prompt", "variables": {}, "template": "hello"}]}
        digest = compute_digest_from_dict(package)
        with tempfile.TemporaryDirectory() as directory:
            cache = Path(directory)
            (cache / digest.replace(":", "_")).write_text(json.dumps(package))
            resolver = PackagedResolver()
            with mock.patch.object(resolver, "_get_cache_dir", return_value=str(cache)), mock.patch("urllib.request.urlopen", side_effect=AssertionError("Schema network access forbidden")):
                self.assertEqual(resolver.resolve("prompt", digest), package["specs"][0])
                changed = {**package, "id": "altered"}
                (cache / digest.replace(":", "_")).write_text(json.dumps(changed))
                resolver.cache.clear()
                with self.assertRaisesRegex(ValueError, "digest"):
                    resolver.resolve("prompt", digest)

    def test_signature_required_blocks_local_and_cached_resolution(self):
        manifest = ManifestWrapper({"version": "1", "prompts": {"prompt": {"id": "prompt", "override": "unused", "require_verification": True}}})
        with mock.patch("promptops.resolver.chain.LocalResolver.resolve", return_value={"id": "prompt"}):
            with self.assertRaisesRegex(NotImplementedError, "verification"):
                ResolverChain().resolve("prompt", manifest)
        resolver = PackagedResolver()
        resolver.cache[("prompt", "https://example.invalid/artifact")] = {"id": "prompt"}
        with self.assertRaisesRegex(NotImplementedError, "verification"):
            resolver.resolve("prompt", "https://example.invalid/artifact", require_verification=True)

    def test_canary_and_observability_are_explicitly_unsupported(self):
        from promptops.runtime.canary import run_canary
        from promptops.runtime.observability import emit_artifacts
        for result in (run_canary("unused"), emit_artifacts("unused")):
            self.assertEqual(result["status"], "unsupported")
        result = subprocess.run([sys.executable, str(ROOT / "bin/apastra"), "canary", "unused"], capture_output=True, text=True)
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(json.loads(result.stdout)["status"], "unsupported")

    def test_community_generator_cannot_write_passing_baselines(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "pack.json"
            path.write_text(json.dumps({"suites": ["demo"]}))
            result = subprocess.run(["bash", str(ROOT / "promptops/harnesses/generate_community_baselines.sh"), str(path)], cwd=directory, env={"PATH": "/usr/bin:/bin", "PYTHON": sys.executable}, capture_output=True, text=True)
            self.assertNotEqual(result.returncode, 0)
            self.assertFalse((Path(directory) / "derived-index/baselines/demo.json").exists())

    def test_legacy_optimizer_cannot_invent_token_savings(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "prompt.json").write_text("{}")
            (root / "manifest.json").write_text("{}")
            result = subprocess.run([sys.executable, str(ROOT / "promptops/harnesses/optimization-analyzer.py"), "--prompt", str(root / "prompt.json"), "--manifest", str(root / "manifest.json"), "--out", str(root / "report.json")], capture_output=True, text=True)
            self.assertNotEqual(result.returncode, 0)
            self.assertFalse((root / "report.json").exists())
