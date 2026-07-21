import json
import os
import shutil
import stat
import subprocess
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]


class RequestLogPackagingTests(unittest.TestCase):
    def test_npm_package_contains_cli_runtime_and_docs(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            result = subprocess.run(
                ["npm", "pack", "--json", "--ignore-scripts", "--pack-destination", temp_dir],
                cwd=REPO_ROOT,
                text=True,
                capture_output=True,
                check=True,
            )
            payload = json.loads(result.stdout)[0]
            files = {item["path"] for item in payload["files"]}

            self.assertIn("bin/apastra", files)
            self.assertIn("promptops/request_log/cli.py", files)
            self.assertIn("promptops/request_log/gateway.py", files)
            self.assertIn("docs/guides/provider-request-logging.md", files)
            self.assertIn("docs/specs/provider-request-logging.md", files)

    def test_git_clone_setup_installs_working_project_local_cli(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            project = Path(temp_dir) / "consumer"
            skill = project / ".agent" / "skills" / "apastra"
            project.mkdir()
            shutil.copytree(
                REPO_ROOT,
                skill,
                ignore=shutil.ignore_patterns(".git", ".venv", "node_modules", "*.tgz", "__pycache__", "*.pyc"),
            )
            environment = {
                **os.environ,
                "APASTRA_ASSUME_YES": "1",
                "APASTRA_NO_SKILL_SYMLINKS": "1",
                "APASTRA_NO_AGENT_HOOKS": "1",
            }
            subprocess.run([str(skill / "setup")], cwd=project, env=environment, text=True, capture_output=True, check=True)

            cli = project / ".agent" / "bin" / "apastra"
            result = subprocess.run(
                [str(cli), "request-log", "status", "--config-dir", str(project / "config"), "--json"],
                cwd=project,
                text=True,
                capture_output=True,
                check=True,
            )
            payload = json.loads(result.stdout)
            self.assertFalse(payload["enabled"])
            self.assertTrue(stat.S_IMODE(cli.stat().st_mode) & stat.S_IXUSR)
            self.assertTrue((project / ".agent" / "scripts" / "apastra" / "request_log" / "gateway.py").is_file())

    def test_source_cli_is_executable(self):
        self.assertTrue(stat.S_IMODE((REPO_ROOT / "bin" / "apastra").stat().st_mode) & stat.S_IXUSR)


if __name__ == "__main__":
    unittest.main()
