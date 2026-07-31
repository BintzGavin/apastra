from __future__ import annotations

import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
HOOK = REPO_ROOT / "promptops/hooks/agent_hook.py"
VALID_PROMPT = REPO_ROOT / "promptops/valid-workspace-prompt.json"
SCHEMAS = REPO_ROOT / "promptops/schemas"


class AgentHookIntegrationTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp_dir = tempfile.TemporaryDirectory()
        self.root = Path(self.temp_dir.name)
        (self.root / "promptops/prompts").mkdir(parents=True)
        shutil.copytree(SCHEMAS, self.root / "promptops/schemas")
        shutil.copy2(VALID_PROMPT, self.root / "promptops/prompts/example.json")
        self._git("init", "-q")
        self._git("add", ".")
        self._git(
            "-c",
            "user.name=Apastra Test",
            "-c",
            "user.email=apastra-test@example.invalid",
            "commit",
            "-qm",
            "test fixture",
        )

    def tearDown(self) -> None:
        self.temp_dir.cleanup()

    def test_unrelated_post_tool_is_silent_with_preexisting_prompt_edit(self) -> None:
        self._update_prompt_description("dirty before the session")
        self._run_hook({"hook_event_name": "SessionStart", "session_id": "quiet-test"})

        result = self._run_hook(
            {
                "hook_event_name": "PostToolUse",
                "session_id": "quiet-test",
                "tool_name": "apply_patch",
                "tool_input": {"file_path": str(self.root / "README.md")},
            }
        )

        self.assertEqual("", result.stdout)
        self.assertEqual([], self._reports())

    def test_prompt_change_is_validated_and_writes_value_free_report(self) -> None:
        self._run_hook({"hook_event_name": "SessionStart", "session_id": "report-test"})
        self._update_prompt_description("changed after session start")

        result = self._run_hook(
            {
                "hook_event_name": "PostToolUse",
                "session_id": "report-test",
                "tool_name": "apply_patch",
                "tool_input": {
                    "file_path": str(self.root / "promptops/prompts/example.json"),
                    "command": "must not be persisted",
                },
                "prompt": "must not be persisted",
            }
        )

        self.assertEqual(0, result.returncode)
        self.assertEqual("", result.stdout)
        reports = self._reports()
        self.assertEqual(1, len(reports))
        report = json.loads(reports[0].read_text())
        self.assertEqual("passed", report["status"])
        self.assertEqual("PostToolUse", report["event"])
        self.assertEqual(["promptops/prompts/example.json"], report["files"])
        self.assertEqual({"checked": 1, "errors": 0, "warnings": 0}, report["counts"])
        serialized = json.dumps(report)
        self.assertNotIn("must not be persisted", serialized)
        self.assertNotIn("changed after session start", serialized)
        self.assertNotIn("report-test", serialized)

    def test_reports_are_append_only_across_relevant_changes(self) -> None:
        self._run_hook({"hook_event_name": "SessionStart", "session_id": "append-test"})
        for description in ("first relevant change", "second relevant change"):
            self._update_prompt_description(description)
            result = self._run_hook(
                {
                    "hook_event_name": "PostToolUse",
                    "session_id": "append-test",
                    "tool_name": "apply_patch",
                    "tool_input": {
                        "file_path": str(self.root / "promptops/prompts/example.json")
                    },
                }
            )
            self.assertEqual("", result.stdout)

        reports = self._reports()
        self.assertEqual(2, len(reports))
        self.assertNotEqual(reports[0].name, reports[1].name)

    def test_invalid_prompt_blocks_and_writes_failed_report(self) -> None:
        self._run_hook({"hook_event_name": "SessionStart", "session_id": "failure-test"})
        (self.root / "promptops/prompts/example.json").write_text("{}\n")

        result = self._run_hook(
            {
                "hook_event_name": "PostToolUse",
                "session_id": "failure-test",
                "tool_name": "apply_patch",
                "tool_input": {"file_path": str(self.root / "promptops/prompts/example.json")},
            }
        )

        response = json.loads(result.stdout)
        self.assertEqual("block", response["decision"])
        reports = self._reports()
        self.assertEqual(1, len(reports))
        report = json.loads(reports[0].read_text())
        self.assertEqual("failed", report["status"])
        self.assertGreater(report["counts"]["errors"], 0)

    def test_installed_schema_bundle_is_used_when_project_schema_dir_is_empty(self) -> None:
        shutil.rmtree(self.root / "promptops/schemas")
        (self.root / "promptops/schemas").mkdir()
        self._run_hook({"hook_event_name": "SessionStart", "session_id": "bundle-test"})
        self._update_prompt_description("validate with bundled schemas")

        result = self._run_hook(
            {
                "hook_event_name": "PostToolUse",
                "session_id": "bundle-test",
                "tool_name": "apply_patch",
                "tool_input": {"file_path": str(self.root / "promptops/prompts/example.json")},
            }
        )

        self.assertEqual(0, result.returncode)
        self.assertEqual("", result.stdout)
        report = json.loads(self._reports()[0].read_text())
        self.assertEqual("passed", report["status"])

    def test_missing_schema_backend_fails_closed(self) -> None:
        installed_hook = (
            self.root / ".agent/scripts/apastra/hooks/agent_hook.py"
        )
        installed_hook.parent.mkdir(parents=True)
        shutil.copy2(HOOK, installed_hook)
        shutil.rmtree(self.root / "promptops/schemas")
        self._run_hook(
            {"hook_event_name": "SessionStart", "session_id": "closed-test"},
            hook=installed_hook,
        )
        self._update_prompt_description("backend is unavailable")

        result = self._run_hook(
            {
                "hook_event_name": "PostToolUse",
                "session_id": "closed-test",
                "tool_name": "apply_patch",
                "tool_input": {"file_path": str(self.root / "promptops/prompts/example.json")},
            },
            hook=installed_hook,
        )

        response = json.loads(result.stdout)
        self.assertEqual("block", response["decision"])
        report = json.loads(self._reports()[0].read_text())
        self.assertEqual("failed", report["status"])

    def test_agent_config_install_ignores_hook_validation_receipts(self) -> None:
        command = [
            sys.executable,
            "-B",
            str(HOOK),
            "--install-agent-configs",
            str(self.root),
            str(HOOK),
        ]
        subprocess.run(command, cwd=self.root, text=True, capture_output=True, check=True)
        subprocess.run(command, cwd=self.root, text=True, capture_output=True, check=True)

        ignore_lines = (self.root / ".gitignore").read_text().splitlines()
        self.assertEqual(1, ignore_lines.count("promptops/runs/hook-validations/"))

    def test_python_syntax_validation_does_not_write_bytecode(self) -> None:
        source = self.root / "promptops/hooks/example.py"
        source.parent.mkdir(parents=True)
        source.write_text("VALUE = 1\n")
        self._git("add", ".")
        self._git(
            "-c",
            "user.name=Apastra Test",
            "-c",
            "user.email=apastra-test@example.invalid",
            "commit",
            "-qm",
            "add python fixture",
        )
        self._run_hook({"hook_event_name": "SessionStart", "session_id": "python-test"})
        source.write_text("VALUE = 2\n")

        result = self._run_hook(
            {
                "hook_event_name": "PostToolUse",
                "session_id": "python-test",
                "tool_name": "apply_patch",
                "tool_input": {"file_path": str(source)},
            }
        )

        self.assertEqual(0, result.returncode)
        self.assertEqual("", result.stdout)
        self.assertFalse((source.parent / "__pycache__").exists())

    def _run_hook(
        self,
        payload: dict[str, object],
        *,
        hook: Path = HOOK,
    ) -> subprocess.CompletedProcess[str]:
        payload.setdefault("cwd", str(self.root))
        return subprocess.run(
            [sys.executable, "-B", str(hook)],
            cwd=self.root,
            input=json.dumps(payload),
            text=True,
            capture_output=True,
            check=False,
        )

    def _update_prompt_description(self, description: str) -> None:
        path = self.root / "promptops/prompts/example.json"
        data = json.loads(path.read_text())
        data["description"] = description
        path.write_text(json.dumps(data, indent=2) + "\n")

    def _reports(self) -> list[Path]:
        reports_dir = self.root / "promptops/runs/hook-validations/reports"
        return sorted(reports_dir.glob("*.json")) if reports_dir.exists() else []

    def _git(self, *args: str) -> None:
        subprocess.run(
            ["git", "-C", str(self.root), *args],
            text=True,
            capture_output=True,
            check=True,
        )


if __name__ == "__main__":
    unittest.main()
