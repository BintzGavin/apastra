"""Exercise the published layout from an unrelated consumer, without network access."""

import json
from pathlib import Path
import shlex
import shutil
import subprocess
import sys
import tempfile
import unittest

from tests.test_evaluation_contract import HARNESS, make_workspace


ROOT = Path(__file__).resolve().parents[1]


def isolated_environment(directory):
    """Use synthetic configuration rather than inheriting developer credentials."""
    directory = Path(directory)
    home = directory / "home"
    home.mkdir(exist_ok=True)
    for name in ("user.npmrc", "global.npmrc"):
        (directory / name).write_text("")
    return {
        "PATH": f"{Path(sys.executable).parent}:/opt/homebrew/bin:/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin",
        "HOME": str(home),
        "TMPDIR": str(directory),
        "PYTHONNOUSERSITE": "1",
        "PYTHONDONTWRITEBYTECODE": "1",
        "npm_config_userconfig": str(directory / "user.npmrc"),
        "npm_config_globalconfig": str(directory / "global.npmrc"),
        "npm_config_cache": str(directory / "npm-cache"),
        "npm_config_offline": "true",
        "npm_config_audit": "false",
        "npm_config_fund": "false",
        "npm_config_update_notifier": "false",
    }


class InstalledContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temporary = tempfile.TemporaryDirectory(prefix="apastra-installed-")
        cls.addClassCleanup(cls.temporary.cleanup)
        cls.directory = Path(cls.temporary.name)
        cls.environment = isolated_environment(cls.directory)
        validator_tools = cls.directory / "validator-tools"
        validator_tools.mkdir()
        node = shutil.which("node", path=cls.environment["PATH"])
        if node is None:
            raise AssertionError("Install Node.js before running packaging acceptance tests")
        (validator_tools / "node").symlink_to(Path(node).resolve())
        for command in ("npm", "npx"):
            stub = validator_tools / command
            stub.write_text("#!/bin/sh\necho 'Unexpected package-manager invocation' >&2\nexit 93\n")
            stub.chmod(0o755)
        cls.validator_environment = {**cls.environment, "PATH": f"{validator_tools}:/usr/bin:/bin"}
        result = subprocess.run(
            ["npm", "pack", "--json", "--ignore-scripts", "--pack-destination", str(cls.directory)],
            cwd=ROOT, env=cls.environment, capture_output=True, text=True, timeout=60,
        )
        if result.returncode:
            raise AssertionError(result.stdout + result.stderr)
        cls.tarball = cls.directory / json.loads(result.stdout)[0]["filename"]

    def test_npm_tarball_supports_evaluation_and_validation_in_both_install_layouts(self):
        for project_setup in (False, True):
            with self.subTest(project_setup=project_setup):
                consumer = self.directory / ("project setup" if project_setup else "default install")
                consumer.mkdir()
                environment = dict(self.environment)
                if project_setup:
                    environment.update({
                        "APASTRA_POSTINSTALL_SETUP": "1",
                        "APASTRA_NO_SKILL_SYMLINKS": "1",
                        "APASTRA_NO_AGENT_HOOKS": "1",
                    })
                # Reuse already installed third-party dependencies as copies. The
                # Apastra code itself must arrive exclusively through npm's tarball.
                shutil.copytree(ROOT / "node_modules", consumer / "node_modules")
                existing = consumer / "node_modules/apastra"
                self.assertFalse(existing.exists(), "Dependencies must not contain an existing Apastra install")
                package = json.loads((ROOT / "package.json").read_text())
                (consumer / "package.json").write_text(json.dumps({
                    "name": "apastra-install-consumer", "private": True,
                    "dependencies": package["dependencies"], "overrides": package["overrides"],
                }))
                installed = subprocess.run(
                    ["npm", "install", "--offline", "--no-audit", "--no-fund", "--foreground-scripts", str(self.tarball)],
                    cwd=consumer, env=environment, capture_output=True, text=True, timeout=60,
                )
                self.assertEqual(installed.returncode, 0, installed.stdout + installed.stderr)
                self.assertEqual((consumer / ".agent").exists(), project_setup)
                self.assertFalse((consumer / ".claude").exists())
                self.assertFalse((consumer / ".codex").exists())
                self.assertFalse((consumer / ".gitignore").exists())
                for path in consumer.rglob("*"):
                    if path.is_symlink():
                        self.assertTrue(path.resolve().is_relative_to(consumer.resolve()), str(path))

                if project_setup:
                    cli = consumer / ".agent/bin/apastra"
                    runtime = consumer / ".agent/scripts/apastra"
                    self.assertTrue((consumer / ".agent/skills/apastra/docs/guides/evaluation-trust.md").is_file())
                else:
                    cli = consumer / "node_modules/.bin/apastra"
                    runtime = consumer / "node_modules/apastra/promptops"
                    self.assertTrue((consumer / "node_modules/apastra/docs/guides/evaluation-trust.md").is_file())
                workspace, adapter = make_workspace(consumer)
                harness = consumer / "deterministic_target.py"
                shutil.copyfile(HARNESS, harness)
                configuration = json.loads(adapter.read_text())
                configuration["entrypoint"] = shlex.join([sys.executable, "-I", str(harness), "valid"])
                adapter.write_text(json.dumps(configuration))

                result = subprocess.run(
                    [sys.executable, "-I", str(cli), "eval", "demo", "--adapter", str(adapter), "--output-dir", str(consumer / "evidence")],
                    cwd=workspace, env=environment, capture_output=True, text=True, timeout=30,
                )
                self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
                decision = json.loads(result.stdout)
                self.assertEqual(decision["status"], "pass")
                self.assertEqual(decision["metrics"], {"exact_match_score": 1.0})
                request = json.loads((consumer / "evidence/run_request.json").read_text())
                self.assertEqual(request["cases"][0]["inputs"], {"text": "hello"})

                for arguments in (["resolve", "prompt"], ["validate", "run-manifest", str(consumer / "evidence/run_manifest.json")], ["gate", str(consumer / "evidence"), "--adapter", str(adapter)]):
                    result = subprocess.run([sys.executable, "-I", str(cli), *arguments], cwd=workspace, env=environment, capture_output=True, text=True, timeout=15)
                    self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

                result = subprocess.run(
                    [sys.executable, "-I", str(cli), "compare", "demo", "--adapter", str(adapter), "--models", "local:uppercase", "local:lowercase", "--output-dir", str(consumer / "comparison")],
                    cwd=workspace, env=environment, capture_output=True, text=True, timeout=30,
                )
                self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
                comparison = json.loads(result.stdout)
                self.assertEqual(comparison["metrics"], {
                    "local:uppercase": {"exact_match_score": 1.0},
                    "local:lowercase": {"exact_match_score": 0.0},
                })
                for run in comparison["runs"].values():
                    self.assertTrue((Path(run) / "cases.jsonl").is_file())

                result = subprocess.run(
                    [str(cli), "request-log", "status", "--config-dir", str(consumer / "config"), "--json"],
                    cwd=workspace, env=environment, capture_output=True, text=True, timeout=15,
                )
                self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
                self.assertFalse(json.loads(result.stdout)["enabled"])

                # Validate actual emitted evidence, then prove malformed evidence
                # fails. No global AJV executable is needed for either layout.
                fixture = consumer / "manifest.json"
                manifest = json.loads((consumer / "evidence/run_manifest.json").read_text())
                for valid in (True, False):
                    with self.subTest(valid_manifest=valid):
                        fixture.write_text(json.dumps(manifest if valid else {}))
                        result = subprocess.run(
                            ["bash", str(runtime / "validators/validate-run-manifest.sh"), str(fixture)],
                            cwd=workspace, env=self.validator_environment, capture_output=True, text=True, timeout=15,
                        )
                        self.assertEqual(result.returncode, 0 if valid else 1, result.stdout + result.stderr)
                        self.assertNotIn("Unexpected package-manager invocation", result.stderr)


if __name__ == "__main__":
    unittest.main()
