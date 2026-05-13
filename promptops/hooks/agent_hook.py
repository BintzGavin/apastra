#!/usr/bin/env python3
"""Shared Apastra hook runner for Codex and Claude Code."""

from __future__ import annotations

import json
import os
import copy
import re
import subprocess
import sys
from pathlib import Path
from typing import Any


APASTRA_CONTEXT = (
    "Apastra PromptOps context: keep prompt assets under promptops/, prefer the "
    "Apastra skills before changing protocol files, and validate prompt specs, "
    "datasets, evaluators, suites, and quick evals after editing them."
)

PROMPT_CONTEXT_TERMS = re.compile(
    r"\b(apastra|promptops|prompt\s+spec|quick\s+eval|dataset|evaluator|suite|baseline|red[- ]team|agent\s+skill)\b",
    re.IGNORECASE,
)

SECRET_PATTERNS = [
    ("OpenAI-style API key", re.compile(r"\bsk-[A-Za-z0-9_-]{20,}\b")),
    ("GitHub token", re.compile(r"\bgh[pousr]_[A-Za-z0-9_]{20,}\b")),
    ("Slack token", re.compile(r"\bxox[abprs]-[A-Za-z0-9-]{20,}\b")),
    ("AWS access key", re.compile(r"\bAKIA[0-9A-Z]{16}\b")),
    ("private key block", re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----")),
]

RISKY_COMMAND_PATTERNS = [
    (
        "destructive removal of project-critical paths",
        re.compile(
            r"\brm\s+-[^\n;&|]*[rf][^\n;&|]*[rf]?[^\n;&|]*(/|~|\$HOME|\.git|\.codex|\.claude|\.agent|promptops)\b"
        ),
    ),
    (
        "remote script piping into a shell",
        re.compile(r"\b(curl|wget)\b[^\n;&|]*(\|\s*|\s+)(sh|bash|zsh)\b", re.IGNORECASE),
    ),
    (
        "world-writable recursive permissions",
        re.compile(r"\bchmod\s+-R\s+777\b", re.IGNORECASE),
    ),
    (
        "direct secret file read",
        re.compile(
            r"\b(cat|sed|awk|grep|rg|less|more)\b[^\n;&|]*(\.env\b|id_rsa|id_ed25519|\.npmrc|\.pypirc)",
            re.IGNORECASE,
        ),
    ),
]

SCHEMA_BY_PREFIX = {
    "promptops/evals/": "quick-eval.schema.json",
    "promptops/evaluators/": "evaluator.schema.json",
    "promptops/suites/": "suite.schema.json",
    "promptops/canaries/": "canary-suite.schema.json",
}


class ValidationReport:
    def __init__(self) -> None:
        self.checked: list[str] = []
        self.errors: list[str] = []
        self.warnings: list[str] = []

    @property
    def failed(self) -> bool:
        return bool(self.errors)

    @property
    def has_signal(self) -> bool:
        return bool(self.checked or self.errors or self.warnings)

    def summary(self) -> str:
        chunks: list[str] = []
        if self.checked:
            chunks.append("Checked:\n" + "\n".join(f"- {item}" for item in self.checked[:20]))
        if self.warnings:
            chunks.append("Warnings:\n" + "\n".join(f"- {item}" for item in self.warnings[:10]))
        if self.errors:
            chunks.append("Errors:\n" + "\n".join(f"- {item}" for item in self.errors[:12]))
        text = "\n\n".join(chunks)
        return text if len(text) <= 6000 else text[:5900] + "\n... output truncated ..."


def main() -> int:
    if len(sys.argv) > 1 and sys.argv[1] == "--install-agent-configs":
        root = Path(sys.argv[2] if len(sys.argv) > 2 else os.getcwd()).resolve()
        hook_script = Path(sys.argv[3]).resolve() if len(sys.argv) > 3 else root / ".agent/scripts/apastra/hooks/agent_hook.py"
        install_agent_configs(root, hook_script)
        return 0

    if len(sys.argv) > 1 and sys.argv[1] in {"--validate-changed", "--validate-all"}:
        root = find_repo_root(Path(os.getcwd()))
        files = all_relevant_files(root) if sys.argv[1] == "--validate-all" else changed_files(root)
        report = validate_files(root, files)
        if report.has_signal:
            print(report.summary())
        return 1 if report.failed else 0

    payload = read_hook_payload()
    event = payload.get("hook_event_name", "")

    if event == "SessionStart":
        emit_context(event, APASTRA_CONTEXT)
        return 0

    if event == "UserPromptSubmit":
        return handle_user_prompt(payload)

    if event in {"PreToolUse", "PermissionRequest"}:
        return handle_pre_tool(payload)

    if event == "PostToolUse":
        return handle_post_tool(payload)

    if event == "Stop":
        return handle_stop(payload)

    return 0


def read_hook_payload() -> dict[str, Any]:
    raw = sys.stdin.read()
    if not raw.strip():
        return {}
    try:
        data = json.loads(raw)
    except json.JSONDecodeError as exc:
        print(f"Apastra hook could not parse JSON input: {exc}", file=sys.stderr)
        return {}
    return data if isinstance(data, dict) else {}


def handle_user_prompt(payload: dict[str, Any]) -> int:
    prompt = str(payload.get("prompt", ""))
    for label, pattern in SECRET_PATTERNS:
        if pattern.search(prompt):
            emit({"decision": "block", "reason": f"Prompt appears to contain a {label}. Remove the secret and retry."})
            return 0

    if PROMPT_CONTEXT_TERMS.search(prompt):
        emit_context("UserPromptSubmit", APASTRA_CONTEXT)
    return 0


def handle_pre_tool(payload: dict[str, Any]) -> int:
    command = tool_command(payload)
    if not command:
        return 0

    for label, pattern in RISKY_COMMAND_PATTERNS:
        if pattern.search(command):
            emit(
                {
                    "hookSpecificOutput": {
                        "hookEventName": payload.get("hook_event_name", "PreToolUse"),
                        "permissionDecision": "deny",
                        "permissionDecisionReason": f"Apastra hook blocked {label}. Ask the user before running it.",
                    }
                }
            )
            return 0
    return 0


def handle_post_tool(payload: dict[str, Any]) -> int:
    root = find_repo_root(Path(payload.get("cwd") or os.getcwd()))
    report = validate_files(root, candidate_files(root, payload))

    if report.failed:
        emit(
            {
                "decision": "block",
                "reason": "Apastra validation failed after the tool ran.\n\n" + report.summary(),
                "hookSpecificOutput": {
                    "hookEventName": "PostToolUse",
                    "additionalContext": "Fix the Apastra validation failures before continuing.",
                },
            }
        )
    elif report.warnings:
        emit_context("PostToolUse", "Apastra hook warning:\n\n" + report.summary())
    return 0


def handle_stop(payload: dict[str, Any]) -> int:
    if payload.get("stop_hook_active"):
        return 0

    root = find_repo_root(Path(payload.get("cwd") or os.getcwd()))
    report = validate_files(root, changed_files(root))

    if report.failed:
        emit({"decision": "block", "reason": "Before stopping, fix Apastra validation failures.\n\n" + report.summary()})
    elif report.warnings:
        emit_context("Stop", "Apastra hook warning:\n\n" + report.summary())
    return 0


def tool_command(payload: dict[str, Any]) -> str:
    tool_input = payload.get("tool_input")
    if isinstance(tool_input, dict):
        value = tool_input.get("command")
        if isinstance(value, str):
            return value
    return ""


def candidate_files(root: Path, payload: dict[str, Any]) -> list[str]:
    files = set(changed_files(root))
    tool_input = payload.get("tool_input")
    if isinstance(tool_input, dict):
        for key in ("file_path", "filePath", "path"):
            value = tool_input.get(key)
            if isinstance(value, str):
                files.add(to_repo_path(root, Path(value)))
    return sorted(path for path in files if path)


def changed_files(root: Path) -> list[str]:
    files: set[str] = set()
    commands = [
        ["git", "-C", str(root), "diff", "--name-only", "--diff-filter=ACMRTUXB", "HEAD", "--"],
        ["git", "-C", str(root), "ls-files", "--others", "--exclude-standard"],
    ]
    for command in commands:
        proc = run(command, root, timeout=10)
        if proc.returncode == 0:
            files.update(line.strip() for line in proc.stdout.splitlines() if line.strip())
    return sorted(files)


def all_relevant_files(root: Path) -> list[str]:
    prefixes = ("promptops/", ".agent/scripts/apastra/")
    files: list[str] = []
    for prefix in prefixes:
        base = root / prefix
        if base.exists():
            files.extend(to_repo_path(root, path) for path in base.rglob("*") if path.is_file())
    return sorted(files)


def validate_files(root: Path, files: list[str]) -> ValidationReport:
    report = ValidationReport()
    relevant = [path for path in files if is_relevant(path)]
    if not relevant:
        return report

    validate_python(root, relevant, report)

    schema_targets = [path for path in relevant if should_schema_validate(path)]
    if schema_targets:
        validator = load_schema_validator(root, report)
        if validator:
            for path in schema_targets:
                validate_structured_file(root, path, validator, report)

    return report


def is_relevant(path: str) -> bool:
    return path.startswith("promptops/") or path.startswith(".agent/scripts/apastra/")


def should_schema_validate(path: str) -> bool:
    suffix = Path(path).suffix.lower()
    if suffix not in {".json", ".jsonl", ".yaml", ".yml"}:
        return False
    return (
        path.startswith("promptops/evals/")
        or path.startswith("promptops/evaluators/")
        or path.startswith("promptops/suites/")
        or path.startswith("promptops/datasets/")
        or path.startswith("promptops/prompts/")
        or path.startswith("promptops/canaries/")
        or path.startswith("promptops/schemas/")
    )


def validate_python(root: Path, files: list[str], report: ValidationReport) -> None:
    py_files = [path for path in files if path.endswith(".py") and (root / path).exists()]
    if not py_files:
        return
    proc = run([sys.executable, "-m", "py_compile", *py_files], root, timeout=30)
    if proc.returncode == 0:
        report.checked.append(f"Python syntax for {len(py_files)} file(s)")
    else:
        report.errors.append("Python syntax check failed:\n" + trim_output(proc.stderr or proc.stdout))


def load_schema_validator(root: Path, report: ValidationReport):
    try:
        import yaml  # type: ignore
        from jsonschema import Draft202012Validator, RefResolver  # type: ignore
    except Exception:
        report.warnings.append("Schema validation skipped; install pyyaml and jsonschema with `python3 -m pip install -r requirements.txt`.")
        return None

    schema_dir = root / "promptops/schemas"
    if not schema_dir.exists():
        report.warnings.append("Schema validation skipped; promptops/schemas was not found.")
        return None

    store: dict[str, Any] = {}
    for schema_path in schema_dir.glob("*.schema.json"):
        try:
            schema = json.loads(schema_path.read_text())
        except Exception as exc:
            report.errors.append(f"{to_repo_path(root, schema_path)} is not valid JSON: {exc}")
            continue
        if isinstance(schema, dict):
            if schema.get("$id"):
                store[str(schema["$id"])] = schema
            store[f"https://promptops.apastra.com/schemas/{schema_path.name}"] = schema
            store[f"https://apastra.com/schemas/promptops/{schema_path.name}"] = schema

    def validate(data: Any, schema_name: str) -> list[str]:
        schema = store.get(f"https://promptops.apastra.com/schemas/{schema_name}") or store.get(
            f"https://apastra.com/schemas/promptops/{schema_name}"
        )
        if not schema:
            return [f"missing schema {schema_name}"]
        resolver = RefResolver.from_schema(schema, store=store)
        validator = Draft202012Validator(schema, resolver=resolver)
        return [error.message for error in sorted(validator.iter_errors(data), key=lambda item: list(item.path))]

    return yaml, validate


def validate_structured_file(root: Path, path: str, validator: Any, report: ValidationReport) -> None:
    full_path = root / path
    if not full_path.exists():
        return

    if path.startswith("promptops/schemas/") and path.endswith(".schema.json"):
        try:
            json.loads(full_path.read_text())
            report.checked.append(path)
        except Exception as exc:
            report.errors.append(f"{path}: invalid JSON schema file: {exc}")
        return

    schema_name = schema_for_path(path)
    if not schema_name:
        return

    yaml_module, validate = validator
    if path.endswith(".jsonl"):
        validate_jsonl(path, full_path, schema_name, validate, report)
        return

    try:
        data = load_yaml_or_json(full_path, yaml_module)
    except Exception as exc:
        report.errors.append(f"{path}: could not parse file: {exc}")
        return

    errors = validate(data, schema_name)
    if errors:
        report.errors.append(f"{path}: " + "; ".join(errors[:5]))
    else:
        report.checked.append(path)


def validate_jsonl(path: str, full_path: Path, schema_name: str, validate: Any, report: ValidationReport) -> None:
    failures: list[str] = []
    for index, line in enumerate(full_path.read_text().splitlines(), start=1):
        if not line.strip():
            continue
        try:
            data = json.loads(line)
        except json.JSONDecodeError as exc:
            failures.append(f"line {index}: invalid JSON: {exc}")
            continue
        errors = validate(data, schema_name)
        failures.extend(f"line {index}: {error}" for error in errors[:3])
    if failures:
        report.errors.append(f"{path}: " + "; ".join(failures[:8]))
    else:
        report.checked.append(path)


def schema_for_path(path: str) -> str | None:
    for prefix, schema in SCHEMA_BY_PREFIX.items():
        if path.startswith(prefix):
            return schema

    if path.startswith("promptops/datasets/"):
        if path.endswith(".jsonl"):
            return "dataset-case.schema.json"
        return "dataset-manifest.schema.json"

    if path.startswith("promptops/prompts/"):
        name = Path(path).name
        if name in {"package.yaml", "package.yml", "package.json"}:
            return "prompt-package.schema.json"
        return "prompt-spec.schema.json"

    return None


def load_yaml_or_json(path: Path, yaml_module: Any) -> Any:
    text = path.read_text()
    if path.suffix.lower() == ".json":
        return json.loads(text)
    return yaml_module.safe_load(text)


def find_repo_root(cwd: Path) -> Path:
    proc = run(["git", "-C", str(cwd), "rev-parse", "--show-toplevel"], cwd, timeout=5)
    if proc.returncode == 0 and proc.stdout.strip():
        return Path(proc.stdout.strip()).resolve()
    return cwd.resolve()


def run(command: list[str], cwd: Path, timeout: int) -> subprocess.CompletedProcess[str]:
    try:
        return subprocess.run(command, cwd=str(cwd), text=True, capture_output=True, timeout=timeout, check=False)
    except Exception as exc:
        return subprocess.CompletedProcess(command, 1, "", str(exc))


def to_repo_path(root: Path, path: Path) -> str:
    try:
        return str(path.resolve().relative_to(root.resolve()))
    except ValueError:
        return str(path)


def trim_output(text: str, limit: int = 2000) -> str:
    text = text.strip()
    return text if len(text) <= limit else text[:limit] + "\n... output truncated ..."


def emit(payload: dict[str, Any]) -> None:
    print(json.dumps(payload, separators=(",", ":")))


def emit_context(event: str, context: str) -> None:
    emit({"hookSpecificOutput": {"hookEventName": event, "additionalContext": context}})


def install_agent_configs(root: Path, hook_script: Path) -> None:
    root.mkdir(parents=True, exist_ok=True)
    install_codex_config(root)
    install_json_hooks(
        root / ".codex/hooks.json",
        "PYTHONDONTWRITEBYTECODE=1 python3 \"$(git rev-parse --show-toplevel)/.agent/scripts/apastra/hooks/agent_hook.py\"",
        codex_hooks(),
    )
    install_json_hooks(
        root / ".claude/settings.json",
        f'PYTHONDONTWRITEBYTECODE=1 python3 "${{CLAUDE_PROJECT_DIR}}/{to_repo_path(root, hook_script)}"',
        claude_hooks(),
    )
    print("Installed Apastra agent hooks for Codex and Claude Code.")


def install_codex_config(root: Path) -> None:
    config_path = root / ".codex/config.toml"
    config_path.parent.mkdir(parents=True, exist_ok=True)
    text = config_path.read_text() if config_path.exists() else ""
    if "codex_hooks" in text:
        text = re.sub(r"codex_hooks\s*=\s*(true|false)", "codex_hooks = true", text)
    elif re.search(r"(?m)^\[features\][ \t]*$", text):
        text = re.sub(r"(?m)^(\[features\][ \t]*)$", "\\1\ncodex_hooks = true", text, count=1)
    else:
        if text and not text.endswith("\n"):
            text += "\n"
        text += "\n[features]\ncodex_hooks = true\n"
    config_path.write_text(text.lstrip())


def install_json_hooks(path: Path, command: str, hooks: dict[str, list[dict[str, Any]]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    data: dict[str, Any] = {}
    if path.exists():
        try:
            parsed = json.loads(path.read_text())
            if isinstance(parsed, dict):
                data = parsed
        except json.JSONDecodeError as exc:
            raise SystemExit(f"Cannot update {path}: invalid JSON ({exc})")

    data.setdefault("hooks", {})
    for event, groups in hooks.items():
        current = data["hooks"].setdefault(event, [])
        for group in groups:
            candidate = copy.deepcopy(group)
            for hook in candidate.get("hooks", []):
                if isinstance(hook, dict) and hook.get("command") == "__APASTRA_COMMAND__":
                    hook["command"] = command
            if not hook_group_exists(current, candidate):
                current.append(candidate)

    path.write_text(json.dumps(data, indent=2) + "\n")


def hook_group_exists(groups: list[Any], candidate: dict[str, Any]) -> bool:
    candidate_commands = [
        hook.get("command")
        for hook in candidate.get("hooks", [])
        if isinstance(hook, dict) and "command" in hook
    ]
    for group in groups:
        if not isinstance(group, dict):
            continue
        for hook in group.get("hooks", []):
            if isinstance(hook, dict) and hook.get("command") in candidate_commands:
                return True
    return False


def codex_hooks() -> dict[str, list[dict[str, Any]]]:
    return {
        "SessionStart": [
            {
                "matcher": "startup|resume|clear",
                "hooks": [
                    {
                        "type": "command",
                        "command": "__APASTRA_COMMAND__",
                        "timeout": 10,
                        "statusMessage": "Loading Apastra context",
                    }
                ],
            }
        ],
        "UserPromptSubmit": [
            {
                "hooks": [
                    {
                        "type": "command",
                        "command": "__APASTRA_COMMAND__",
                        "timeout": 10,
                        "statusMessage": "Checking Apastra prompt context",
                    }
                ]
            }
        ],
        "PreToolUse": [
            {
                "matcher": "Bash",
                "hooks": [
                    {
                        "type": "command",
                        "command": "__APASTRA_COMMAND__",
                        "timeout": 10,
                        "statusMessage": "Checking Bash safety",
                    }
                ],
            }
        ],
        "PostToolUse": [
            {
                "matcher": "Bash|apply_patch",
                "hooks": [
                    {
                        "type": "command",
                        "command": "__APASTRA_COMMAND__",
                        "timeout": 60,
                        "statusMessage": "Validating Apastra changes",
                    }
                ],
            }
        ],
        "Stop": [
            {
                "hooks": [
                    {
                        "type": "command",
                        "command": "__APASTRA_COMMAND__",
                        "timeout": 60,
                        "statusMessage": "Checking Apastra validation",
                    }
                ]
            }
        ],
    }


def claude_hooks() -> dict[str, list[dict[str, Any]]]:
    hooks = codex_hooks()
    hooks["SessionStart"][0]["matcher"] = "startup|resume|clear|compact"
    hooks["PostToolUse"][0]["matcher"] = "Bash|Edit|MultiEdit|Write"
    return hooks


if __name__ == "__main__":
    raise SystemExit(main())
