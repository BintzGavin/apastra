"""Exercise the published layout from an unrelated consumer, without network access."""

import json
import asyncio
from pathlib import Path
import shlex
import shutil
import subprocess
import sys
import tempfile
import sysconfig
import venv
import zipfile
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
                self.assertTrue((runtime / "runtime/mcp_launcher.py").is_file())
                for name in ("run.py", "adapter.yaml", "README.md"):
                    self.assertTrue((runtime / "harnesses/promptfoo" / name).is_file())
                bridge = runtime / "harnesses/promptfoo/run.py"
                imported = subprocess.run([sys.executable, "-I", "-c",
                                           "import runpy, sys; module = runpy.run_path(sys.argv[1], run_name='installed_bridge'); "
                                           "assert callable(module['main'])", str(bridge)], cwd=consumer,
                                          env=environment, text=True, capture_output=True, timeout=15)
                self.assertEqual(imported.returncode, 0, imported.stdout + imported.stderr)
                self.assertTrue((consumer / "node_modules/apastra/requirements-mcp.txt").is_file())
                self.assertTrue((consumer / "node_modules/apastra/promptops/integrations/kody/apastra/start.ts").is_file())
                workspace, adapter = make_workspace(consumer)
                asyncio.run(verify_installed_mcp(cli, workspace, environment))
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


class PythonInstalledContractTests(unittest.TestCase):
    def test_wheel_runs_without_node_from_an_unrelated_consumer(self):
        with tempfile.TemporaryDirectory(prefix="apastra-wheel-") as directory:
            directory = Path(directory)
            environment = isolated_environment(directory)
            source = directory / "source"
            shutil.copytree(ROOT, source, ignore=shutil.ignore_patterns(
                ".git", ".venv", "node_modules", "*.tgz", "__pycache__", "*.pyc", "build", "*.egg-info"))
            self.assertTrue((source / "pyproject.toml").is_file(), "A normal Python package is required")
            (source / "promptops/manifests/experimental-results.yaml").write_text("score: 0.5\n")
            (source / "promptops/harnesses/promptfoo/experimental-results.yaml").write_text("score: 0.5\n")
            (source / "promptops/schemas/experimental-results.json").write_text('{"score": 0.5}')
            wheelhouse = directory / "wheelhouse"
            wheelhouse.mkdir()
            # Prefer the running interpreter; accept a system backend only when
            # it supports the PEP 621 metadata declared by this package.
            backend = None
            for candidate in (sys.executable, "/usr/bin/python3"):
                check = subprocess.run([candidate, "-c", "import setuptools, wheel; assert int(setuptools.__version__.split('.')[0]) >= 61"], env=environment,
                                       capture_output=True, text=True)
                if check.returncode == 0:
                    backend = candidate
                    break
            self.assertIsNotNone(backend, "Offline setuptools and wheel are required for wheel acceptance")
            built = subprocess.run([backend, "-c", "from setuptools.build_meta import build_wheel; "
                                    "import sys; build_wheel(sys.argv[1])", str(wheelhouse)],
                                   cwd=source, env=environment, text=True, capture_output=True, timeout=60)
            self.assertEqual(built.returncode, 0, built.stdout + built.stderr)
            wheel, = wheelhouse.glob("*.whl")
            with zipfile.ZipFile(wheel) as archive:
                names = set(archive.namelist())
                self.assertIn("promptops/schemas/run-manifest.schema.json", names)
                self.assertIn("promptops/runtime/entrypoint.py", names)
                for name in ("run.py", "adapter.yaml", "README.md"):
                    self.assertIn(f"promptops/harnesses/promptfoo/{name}", names)
                self.assertFalse(any("/runs/" in name and name.endswith((".json", ".jsonl")) for name in names))
                self.assertFalse(any("experimental" in name or "node_modules" in name for name in names))
            consumer = directory / "consumer"
            venv.EnvBuilder(with_pip=False).create(consumer)
            python = consumer / "bin/python"
            # Reuse existing interpreter dependencies without a network resolver.
            site = subprocess.run([str(python), "-c", "import sysconfig; print(sysconfig.get_path('purelib'))"],
                                  env=environment, text=True, capture_output=True, check=True).stdout.strip()
            (Path(site) / "existing-dependencies.pth").write_text(sysconfig.get_path("purelib") + "\n")
            installed = subprocess.run([sys.executable, "-m", "pip", "--python", str(python), "install",
                                        "--no-deps", "--no-index", str(wheel)], cwd=directory,
                                       env=environment, capture_output=True, text=True, timeout=60)
            self.assertEqual(installed.returncode, 0, installed.stdout + installed.stderr)
            shutil.rmtree(source)
            unrelated = directory / "unrelated"
            unrelated.mkdir()
            bridge = Path(site) / "promptops/harnesses/promptfoo/run.py"
            imported = subprocess.run([str(python), "-I", "-c",
                                       "import runpy, sys; module = runpy.run_path(sys.argv[1], run_name='installed_bridge'); "
                                       "assert callable(module['main'])", str(bridge)], cwd=unrelated,
                                      env=environment, text=True, capture_output=True, timeout=15)
            self.assertEqual(imported.returncode, 0, imported.stdout + imported.stderr)
            cli = consumer / "bin/apastra"
            node_guard = directory / "node-guard"
            node_guard.mkdir()
            for command in ("node", "npm", "npx"):
                stub = node_guard / command
                stub.write_text("#!/bin/sh\necho 'Unexpected Node invocation' >&2\nexit 93\n")
                stub.chmod(0o755)
            environment["PATH"] = f"{node_guard}:/usr/bin:/bin"
            for arguments in (["--help"], ["request-log", "status", "--config-dir", str(unrelated / "config"), "--json"]):
                result = subprocess.run([str(cli), *arguments], cwd=unrelated, env=environment,
                                        capture_output=True, text=True, timeout=15)
                self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            workspace, adapter = make_workspace(unrelated)
            harness = unrelated / "deterministic_target.py"
            shutil.copyfile(HARNESS, harness)
            configuration = json.loads(adapter.read_text())
            configuration["entrypoint"] = shlex.join([str(python), "-I", str(harness), "valid"])
            adapter.write_text(json.dumps(configuration))
            result = subprocess.run([str(cli), "eval", "demo", "--adapter", str(adapter), "--output-dir", str(unrelated / "evidence")],
                                    cwd=workspace, env=environment, capture_output=True, text=True, timeout=30)
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertEqual(json.loads(result.stdout)["metrics"], {"exact_match_score": 1.0})
            result = subprocess.run([str(cli), "validate", "run-manifest", str(unrelated / "evidence/run_manifest.json")],
                                    cwd=workspace, env=environment, capture_output=True, text=True, timeout=15)
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)


async def verify_installed_mcp(cli, workspace, environment):
    """The packed launcher must serve MCP independently of this source checkout."""
    from mcp import ClientSession, StdioServerParameters
    from mcp.client.stdio import stdio_client
    parameters = StdioServerParameters(command=sys.executable, args=["-I", str(cli), "mcp", "--workspace", str(workspace), "--workspace-id", "installed"], env=environment)
    with (workspace / "mcp-diagnostics.txt").open("w") as diagnostics:
        async with stdio_client(parameters, errlog=diagnostics) as streams:
            async with ClientSession(*streams) as client:
                await client.initialize()
                names = {tool.name for tool in (await client.list_tools()).tools}
                if not {"start_evaluation", "compare_runs", "get_case"} <= names:
                    raise AssertionError("Installed tools are missing")
                info = await client.call_tool("workspace_info", {})
                if info.isError or info.structuredContent["workspace_id"] != "installed":
                    raise AssertionError("Installed workspace selection failed")


if __name__ == "__main__":
    unittest.main()
