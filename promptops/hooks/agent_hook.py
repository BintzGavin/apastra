#!/usr/bin/env python3
"""Shared Apastra hook runner for Codex and Claude Code."""

from __future__ import annotations

import copy
import json
import os
import re
import subprocess
import sys
import uuid
from datetime import datetime, timezone
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

HOOK_VALIDATION_ROOT = "promptops/runs/hook-validations"
HOOK_OUTPUT_PREFIXES = (
    f"{HOOK_VALIDATION_ROOT}/",
)


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
        return handle_session_start(payload)

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


def handle_session_start(payload: dict[str, Any]) -> int:
    root = find_repo_root(Path(payload.get("cwd") or os.getcwd()))
    save_relevant_snapshot(root, payload, capture_relevant_snapshot(root))
    emit_context("SessionStart", APASTRA_CONTEXT)
    return 0


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
    previous = load_relevant_snapshot(root, payload)
    current = capture_relevant_snapshot(root)
    files = (
        changed_since_snapshot(previous, current)
        if previous is not None
        else candidate_files(root, payload)
    )
    save_relevant_snapshot(root, payload, current)
    report = validate_files(root, files)

    if files:
        persist_validation_report(root, "PostToolUse", files, report)

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
    files = [path for path in changed_files(root) if is_watchable(path)]
    report = validate_files(root, files)

    if files:
        persist_validation_report(root, "Stop", files, report)

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
    files: set[str] = set()
    tool_input = payload.get("tool_input")
    if isinstance(tool_input, dict):
        for key in ("file_path", "filePath", "path"):
            value = tool_input.get(key)
            if isinstance(value, str):
                files.add(to_repo_path(root, Path(value)))
    return sorted(path for path in files if path and is_watchable(path))


def capture_relevant_snapshot(root: Path) -> dict[str, list[int]]:
    snapshot: dict[str, list[int]] = {}
    for prefix in ("promptops", ".agent/scripts/apastra"):
        base = root / prefix
        if not base.exists():
            continue
        for path in base.rglob("*"):
            if not path.is_file():
                continue
            repo_path = to_repo_path(root, path)
            if not is_watchable(repo_path):
                continue
            stat = path.stat()
            snapshot[repo_path] = [stat.st_mtime_ns, stat.st_size]
    return snapshot


def changed_since_snapshot(
    previous: dict[str, list[int]],
    current: dict[str, list[int]],
) -> list[str]:
    paths = set(previous) | set(current)
    return sorted(path for path in paths if previous.get(path) != current.get(path))


def hook_state_path(root: Path, payload: dict[str, Any]) -> Path:
    raw_session_id = str(payload.get("session_id") or "default")
    session_id = re.sub(r"[^A-Za-z0-9_.-]", "_", raw_session_id)[:80] or "default"
    return root / HOOK_VALIDATION_ROOT / "state" / f"{session_id}.json"


def load_relevant_snapshot(root: Path, payload: dict[str, Any]) -> dict[str, list[int]] | None:
    path = hook_state_path(root, payload)
    if not path.exists():
        return None
    try:
        data = json.loads(path.read_text())
    except (OSError, json.JSONDecodeError):
        return None
    if not isinstance(data, dict):
        return None
    return {
        str(key): value
        for key, value in data.items()
        if isinstance(key, str)
        and isinstance(value, list)
        and len(value) == 2
        and all(isinstance(item, int) for item in value)
    }


def save_relevant_snapshot(
    root: Path,
    payload: dict[str, Any],
    snapshot: dict[str, list[int]],
) -> None:
    path = hook_state_path(root, payload)
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(f".{path.name}.{uuid.uuid4().hex}.tmp")
    temporary.write_text(json.dumps(snapshot, sort_keys=True, separators=(",", ":")) + "\n")
    temporary.replace(path)


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
    relevant = [path for path in files if is_watchable(path)]
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


def is_watchable(path: str) -> bool:
    if not is_relevant(path):
        return False
    if any(path.startswith(prefix) for prefix in HOOK_OUTPUT_PREFIXES):
        return False
    return "/__pycache__/" not in f"/{path}" and not path.endswith((".pyc", ".pyo"))


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
    passed = 0
    for path in py_files:
        try:
            source = (root / path).read_text()
            compile(source, path, "exec")
            passed += 1
        except SyntaxError as exc:
            location = f"line {exc.lineno}" if exc.lineno else "unknown line"
            report.errors.append(f"{path}: Python syntax error at {location}: {exc.msg}")
        except (OSError, UnicodeError) as exc:
            report.errors.append(f"{path}: Python source could not be read: {type(exc).__name__}")
    if passed:
        report.checked.append(f"Python syntax for {passed} file(s)")


def load_schema_validator(root: Path, report: ValidationReport):
    node_script = Path(__file__).with_name("schema_validator.js")
    if node_script.exists():
        probe = run(["node", str(node_script), "--probe"], root, timeout=10)
        if probe.returncode == 0:
            return "node", node_script

    try:
        import yaml  # type: ignore
        from jsonschema import RefResolver, validators  # type: ignore
    except Exception:
        report.errors.append(
            "Schema validation unavailable: install Apastra's Node dependencies or provide pyyaml and jsonschema."
        )
        return None

    schema_dir = find_schema_dir(root)
    if schema_dir is None:
        report.errors.append("Schema validation unavailable: Apastra schemas were not found.")
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
        validator_class = validators.validator_for(schema)
        validator = validator_class(schema, resolver=resolver)
        return [
            safe_jsonschema_error(error)
            for error in sorted(validator.iter_errors(data), key=lambda item: list(item.path))
        ]

    return "python", yaml, validate


def safe_jsonschema_error(error: Any) -> str:
    location = "/" + "/".join(str(item) for item in error.path) if error.path else "/"
    validator = str(error.validator or "schema")
    return f"{location}: failed {validator} validation"


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

    if validator[0] == "node":
        validate_structured_file_with_node(root, path, schema_name, validator[1], report)
        return

    _, yaml_module, validate = validator
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


def validate_structured_file_with_node(
    root: Path,
    path: str,
    schema_name: str,
    node_script: Path,
    report: ValidationReport,
) -> None:
    schema_dir = find_schema_dir(root, schema_name)
    if schema_dir is None:
        report.errors.append(f"{path}: schema directory was not found")
        return

    mode = "jsonl" if path.endswith(".jsonl") else "document"
    proc = run(
        [
            "node",
            str(node_script),
            str(schema_dir),
            schema_name,
            str(root / path),
            mode,
        ],
        root,
        timeout=30,
    )
    try:
        result = json.loads(proc.stdout)
    except json.JSONDecodeError:
        result = {}

    if proc.returncode == 0 and result.get("status") == "pass":
        report.checked.append(path)
        return

    if proc.returncode == 1 and result.get("status") == "fail":
        errors = result.get("errors")
        messages = [
            str(item)
            for item in errors
            if isinstance(item, str)
        ] if isinstance(errors, list) else []
        detail = "; ".join(messages[:8]) or "schema validation failed"
        report.errors.append(f"{path}: {detail}")
        return

    report.errors.append(
        f"{path}: schema validation backend failed; verify Apastra's Node dependencies"
    )


def find_schema_dir(root: Path, schema_name: str | None = None) -> Path | None:
    candidates = [
        root / "promptops/schemas",
        Path(__file__).resolve().parent.parent / "schemas",
    ]
    for path in candidates:
        if not path.is_dir():
            continue
        if schema_name is None and any(path.glob("*.schema.json")):
            return path
        if schema_name is not None and (path / schema_name).is_file():
            return path
    return None


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


def persist_validation_report(
    root: Path,
    event: str,
    files: list[str],
    report: ValidationReport,
) -> Path:
    recorded_at = datetime.now(timezone.utc)
    if report.errors:
        status = "failed"
    elif report.warnings:
        status = "warning"
    elif report.checked:
        status = "passed"
    else:
        status = "skipped"
    record = {
        "schema_version": "1.0",
        "record_type": "apastra-hook-validation",
        "recorded_at": recorded_at.isoformat().replace("+00:00", "Z"),
        "event": event,
        "status": status,
        "files": sorted(set(files)),
        "counts": {
            "checked": len(report.checked),
            "errors": len(report.errors),
            "warnings": len(report.warnings),
        },
    }
    reports_dir = root / HOOK_VALIDATION_ROOT / "reports"
    reports_dir.mkdir(parents=True, exist_ok=True)
    timestamp = recorded_at.strftime("%Y%m%dT%H%M%S.%fZ")
    path = reports_dir / f"{timestamp}-{uuid.uuid4().hex[:8]}.json"
    path.write_text(json.dumps(record, indent=2, sort_keys=True) + "\n")
    return path


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
    install_hook_gitignore(root)
    hook_relpath = to_repo_path(root, hook_script)
    install_json_hooks(
        root / ".codex/hooks.json",
        f'PYTHONDONTWRITEBYTECODE=1 python3 "$(git rev-parse --show-toplevel)/{hook_relpath}"',
        codex_hooks(),
    )
    install_json_hooks(
        root / ".claude/settings.json",
        f'PYTHONDONTWRITEBYTECODE=1 python3 "${{CLAUDE_PROJECT_DIR}}/{hook_relpath}"',
        claude_hooks(),
    )
    print("Installed Apastra agent hooks for Codex and Claude Code.")


def install_hook_gitignore(root: Path) -> None:
    path = root / ".gitignore"
    text = path.read_text() if path.exists() else ""
    entry = f"{HOOK_VALIDATION_ROOT}/"
    if entry in text.splitlines():
        return
    if text and not text.endswith("\n"):
        text += "\n"
    path.write_text(text + entry + "\n")


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
            existing = find_matching_hook_group(current, candidate)
            if existing:
                merge_hook_group_metadata(existing, candidate)
            else:
                current.append(candidate)

    path.write_text(json.dumps(data, indent=2) + "\n")


def find_matching_hook_group(groups: list[Any], candidate: dict[str, Any]) -> dict[str, Any] | None:
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
                return group
    return None


def merge_hook_group_metadata(existing: dict[str, Any], candidate: dict[str, Any]) -> None:
    if not existing.get("name") and candidate.get("name"):
        existing["name"] = candidate["name"]

    candidate_by_command = {
        hook.get("command"): hook
        for hook in candidate.get("hooks", [])
        if isinstance(hook, dict) and hook.get("command")
    }
    for hook in existing.get("hooks", []):
        if not isinstance(hook, dict):
            continue
        candidate_hook = candidate_by_command.get(hook.get("command"))
        if not candidate_hook:
            continue
        if not hook.get("name") and candidate_hook.get("name"):
            hook["name"] = candidate_hook["name"]


def codex_hooks() -> dict[str, list[dict[str, Any]]]:
    return {
        "SessionStart": [
            {
                "name": "Apastra session context",
                "matcher": "startup|resume|clear",
                "hooks": [
                    {
                        "name": "Apastra: load session context",
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
                "name": "Apastra prompt context",
                "hooks": [
                    {
                        "name": "Apastra: check prompt context",
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
                "name": "Apastra Bash safety",
                "matcher": "Bash",
                "hooks": [
                    {
                        "name": "Apastra: check Bash safety",
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
                "name": "Apastra PromptOps validation",
                "matcher": "Bash|apply_patch",
                "hooks": [
                    {
                        "name": "Apastra: validate PromptOps changes",
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
                "name": "Apastra stop validation",
                "hooks": [
                    {
                        "name": "Apastra: check final validation",
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
