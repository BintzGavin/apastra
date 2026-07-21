from __future__ import annotations

import hashlib
import json
import os
import re
import shutil
import tempfile
from dataclasses import dataclass, field
from pathlib import Path
from typing import Callable

from .config import SUPPORTED_ADAPTERS, _chmod_private, _write_private


@dataclass
class SessionLaunch:
    command: list[str]
    environment: dict[str, str] = field(default_factory=dict)
    _cleanup: Callable[[], None] = lambda: None

    def cleanup(self) -> None:
        self._cleanup()


def provider_base(gateway: str, provider: str, adapter: str) -> str:
    gateway = gateway.rstrip("/")
    suffix = f"/{provider}/{adapter}"
    if provider == "openai" or adapter in {"opencode", "pi"}:
        suffix += "/v1"
    return gateway + suffix


def build_session_launch(
    adapter: str,
    arguments: list[str],
    gateway: str,
    providers: list[str],
    parent_environment: dict[str, str] | None = None,
    pi_agent_dir: Path | None = None,
    temp_root: Path | None = None,
) -> SessionLaunch:
    _validate_selection(adapter, providers)
    parent = parent_environment if parent_environment is not None else os.environ

    if adapter == "codex":
        return SessionLaunch(
            ["codex", "-c", f'openai_base_url="{provider_base(gateway, "openai", adapter)}"', *arguments]
        )
    if adapter == "claude-code":
        return SessionLaunch(
            ["claude", *arguments],
            {"ANTHROPIC_BASE_URL": provider_base(gateway, "anthropic", adapter)},
        )
    if adapter == "opencode":
        inline: dict = {}
        if parent.get("OPENCODE_CONFIG_CONTENT"):
            try:
                parsed = json.loads(parent["OPENCODE_CONFIG_CONTENT"])
                if isinstance(parsed, dict):
                    inline = parsed
            except json.JSONDecodeError as exc:
                raise ValueError("OPENCODE_CONFIG_CONTENT is not valid JSON") from exc
        provider_config = _object_field(inline, "provider", "OpenCode provider configuration")
        for provider in providers:
            provider_settings = _object_field(provider_config, provider, f"OpenCode {provider} provider configuration")
            options = _object_field(provider_settings, "options", f"OpenCode {provider} provider options")
            options["baseURL"] = provider_base(gateway, provider, adapter)
        return SessionLaunch(
            ["opencode", *arguments],
            {"OPENCODE_CONFIG_CONTENT": json.dumps(inline, separators=(",", ":"))},
        )
    if adapter == "pi":
        source = (pi_agent_dir or Path(parent.get("PI_CODING_AGENT_DIR", Path.home() / ".pi" / "agent"))).expanduser()
        base_temp = temp_root.expanduser() if temp_root is not None else None
        if base_temp is not None:
            base_temp.mkdir(parents=True, exist_ok=True)
        isolated = Path(tempfile.mkdtemp(prefix="apastra-pi-", dir=str(base_temp) if base_temp else None))
        _chmod_private(isolated, directory=True)
        if source.exists():
            for entry in source.iterdir():
                if entry.name == "models.json":
                    continue
                destination = isolated / entry.name
                try:
                    destination.symlink_to(entry, target_is_directory=entry.is_dir())
                except OSError:
                    if entry.is_dir():
                        shutil.copytree(entry, destination)
                    else:
                        shutil.copy2(entry, destination)
        models: dict = {}
        models_path = source / "models.json"
        if models_path.is_file():
            parsed = json.loads(models_path.read_text(encoding="utf-8"))
            if not isinstance(parsed, dict):
                raise ValueError("Pi models.json must contain a JSON object")
            models = parsed
        model_providers = _object_field(models, "providers", "Pi providers configuration")
        for provider in providers:
            provider_settings = _object_field(model_providers, provider, f"Pi {provider} provider configuration")
            provider_settings["baseUrl"] = provider_base(gateway, provider, adapter)
        _write_private(isolated / "models.json", json.dumps(models, indent=2).encode("utf-8") + b"\n")
        return SessionLaunch(
            ["pi", *arguments],
            {"PI_CODING_AGENT_DIR": str(isolated)},
            lambda: shutil.rmtree(isolated, ignore_errors=True),
        )
    if adapter == "generic":
        if not arguments:
            raise ValueError("Generic adapter requires a command after --")
        environment: dict[str, str] = {}
        if "openai" in providers:
            environment["OPENAI_BASE_URL"] = provider_base(gateway, "openai", adapter)
        if "anthropic" in providers:
            environment["ANTHROPIC_BASE_URL"] = provider_base(gateway, "anthropic", adapter)
        return SessionLaunch(list(arguments), environment)
    raise ValueError(f"Unknown adapter: {adapter}")


def persistent_config_bytes(adapter: str, original: bytes, gateway: str, providers: list[str]) -> bytes:
    selected = [provider for provider in providers if provider in SUPPORTED_ADAPTERS.get(adapter, set())]
    _validate_selection(adapter, selected)
    if adapter == "codex":
        return _set_toml_top_level(
            original,
            "openai_base_url",
            provider_base(gateway, "openai", adapter),
        )

    try:
        text = original.decode("utf-8-sig")
        if adapter == "opencode":
            text = _strip_jsonc(text)
        data = json.loads(text) if text.strip() else {}
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise ValueError(f"{adapter} configuration is not valid JSON") from exc
    if not isinstance(data, dict):
        raise ValueError(f"{adapter} configuration must contain a JSON object")
    if adapter == "claude-code":
        environment = _object_field(data, "env", "Claude Code env configuration")
        environment["ANTHROPIC_BASE_URL"] = provider_base(gateway, "anthropic", adapter)
    elif adapter == "opencode":
        provider_config = _object_field(data, "provider", "OpenCode provider configuration")
        for provider in selected:
            provider_settings = _object_field(provider_config, provider, f"OpenCode {provider} provider configuration")
            options = _object_field(provider_settings, "options", f"OpenCode {provider} provider options")
            options["baseURL"] = provider_base(gateway, provider, adapter)
    elif adapter == "pi":
        provider_config = _object_field(data, "providers", "Pi providers configuration")
        for provider in selected:
            provider_settings = _object_field(provider_config, provider, f"Pi {provider} provider configuration")
            provider_settings["baseUrl"] = provider_base(gateway, provider, adapter)
    elif adapter == "generic":
        environment = _object_field(data, "environment", "generic environment configuration")
        if "openai" in selected:
            environment["OPENAI_BASE_URL"] = provider_base(gateway, "openai", adapter)
        if "anthropic" in selected:
            environment["ANTHROPIC_BASE_URL"] = provider_base(gateway, "anthropic", adapter)
    else:
        raise ValueError(f"Unknown adapter: {adapter}")
    return json.dumps(data, indent=2, sort_keys=True).encode("utf-8") + b"\n"


class ManagedConfigInstall:
    def __init__(self, state_root: Path | str, adapter: str, target: Path | str):
        self.root = Path(state_root).expanduser().resolve() / adapter
        self.target = Path(target).expanduser().resolve()
        self.backup_path = self.root / "original.bin"
        self.manifest_path = self.root / "install.json"

    def apply(self, applied: bytes) -> None:
        if self.manifest_path.exists():
            self.ensure_restorable()
            if _digest(applied) != self._manifest()["applied_digest"]:
                raise RuntimeError(
                    f"disable request logging for {self.root.name} before changing its persistent provider routes"
                )
            return
        existed = self.target.exists()
        original = self.target.read_bytes() if existed else b""
        try:
            self.root.mkdir(parents=True, exist_ok=True, mode=0o700)
            _chmod_private(self.root, directory=True)
            _write_private(self.backup_path, original)
            manifest = {
                "schema_version": 1,
                "adapter": self.root.name,
                "target": str(self.target),
                "target_existed": existed,
                "original_digest": _digest(original),
                "applied_digest": _digest(applied),
            }
            _write_private(self.manifest_path, json.dumps(manifest, indent=2, sort_keys=True).encode("utf-8") + b"\n")
            self.target.parent.mkdir(parents=True, exist_ok=True, mode=0o700)
            _write_atomic_private(self.target, applied)
        except Exception:
            try:
                current = self.target.read_bytes() if self.target.exists() else b""
                if _digest(current) == _digest(applied):
                    if existed:
                        _write_atomic_private(self.target, original)
                    elif self.target.exists():
                        self.target.unlink()
            finally:
                shutil.rmtree(self.root, ignore_errors=True)
            raise

    def ensure_restorable(self) -> bool:
        if not self.manifest_path.exists():
            return False
        manifest = self._manifest()
        current = self.target.read_bytes() if self.target.exists() else b""
        if _digest(current) != manifest["applied_digest"]:
            raise RuntimeError(f"{self.target} changed after Apastra installed request logging")
        try:
            original = self.backup_path.read_bytes()
        except OSError as exc:
            raise RuntimeError(f"Apastra request-log backup is unavailable for {self.target}") from exc
        if _digest(original) != manifest["original_digest"]:
            raise RuntimeError(f"Apastra request-log backup is corrupted for {self.target}")
        return True

    def restore(self) -> None:
        if not self.ensure_restorable():
            return
        manifest = self._manifest()
        original = self.backup_path.read_bytes()
        if manifest["target_existed"]:
            _write_atomic_private(self.target, original)
        elif self.target.exists():
            self.target.unlink()
        shutil.rmtree(self.root)

    def _manifest(self) -> dict:
        data = json.loads(self.manifest_path.read_text(encoding="utf-8"))
        if not isinstance(data, dict):
            raise ValueError("Invalid request-log install state")
        required = {"schema_version", "adapter", "target", "target_existed", "original_digest", "applied_digest"}
        if not required.issubset(data) or data["schema_version"] != 1 or data["target"] != str(self.target):
            raise ValueError("Invalid request-log install state")
        return data


def _validate_selection(adapter: str, providers: list[str]) -> None:
    if adapter not in SUPPORTED_ADAPTERS:
        raise ValueError(f"Unknown adapter: {adapter}")
    if not providers:
        raise ValueError(f"No supported provider selected for {adapter}")
    unsupported = set(providers) - SUPPORTED_ADAPTERS[adapter]
    if unsupported:
        raise ValueError(f"Adapter {adapter} does not support: {', '.join(sorted(unsupported))}")


def _object_field(container: dict, key: str, description: str) -> dict:
    value = container.setdefault(key, {})
    if not isinstance(value, dict):
        raise ValueError(f"{description} must be an object")
    return value


def _strip_jsonc(text: str) -> str:
    output: list[str] = []
    index = 0
    in_string = False
    escaped = False
    while index < len(text):
        character = text[index]
        next_character = text[index + 1] if index + 1 < len(text) else ""
        if in_string:
            output.append(character)
            if escaped:
                escaped = False
            elif character == "\\":
                escaped = True
            elif character == '"':
                in_string = False
            index += 1
            continue
        if character == '"':
            in_string = True
            output.append(character)
            index += 1
            continue
        if character == "/" and next_character == "/":
            index += 2
            while index < len(text) and text[index] not in "\r\n":
                index += 1
            continue
        if character == "/" and next_character == "*":
            index += 2
            while index + 1 < len(text) and text[index : index + 2] != "*/":
                index += 1
            index += 2
            continue
        output.append(character)
        index += 1
    return re.sub(r",(?=\s*[}\]])", "", "".join(output))


def _set_toml_top_level(original: bytes, key: str, value: str) -> bytes:
    text = original.decode("utf-8")
    lines = text.splitlines()
    replacement = f'{key} = {json.dumps(value)}'
    found = False
    in_table = False
    output: list[str] = []
    for line in lines:
        stripped = line.strip()
        if stripped.startswith("["):
            in_table = True
        if not in_table and stripped.split("=", 1)[0].strip() == key if "=" in stripped else False:
            if not found:
                output.append(replacement)
                found = True
            continue
        output.append(line)
    if not found:
        insert_at = next((index for index, line in enumerate(output) if line.strip().startswith("[")), len(output))
        output.insert(insert_at, replacement)
    return ("\n".join(output).rstrip("\n") + "\n").encode("utf-8")


def _digest(data: bytes) -> str:
    return "sha256:" + hashlib.sha256(data).hexdigest()


def _write_atomic_private(path: Path, data: bytes) -> None:
    temp = path.with_name(f".{path.name}.{os.getpid()}.apastra.tmp")
    _write_private(temp, data)
    os.replace(temp, path)
    _chmod_private(path, directory=False)
