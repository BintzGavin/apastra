from __future__ import annotations

import ipaddress
import json
import os
import sys
from dataclasses import asdict, dataclass, field, fields, replace
from pathlib import Path
from typing import Any
from urllib.parse import urlsplit


SCHEMA_VERSION = 1
DEFAULT_RETENTION_DAYS = 7
DEFAULT_MAX_BYTES = 250 * 1024 * 1024
DEFAULT_PORT = 43123
SUPPORTED_ADAPTERS = {
    "codex": {"openai"},
    "claude-code": {"anthropic"},
    "opencode": {"openai", "anthropic"},
    "pi": {"openai", "anthropic"},
    "generic": {"openai", "anthropic"},
}
SUPPORTED_PROVIDERS = {"openai", "anthropic"}
DEFAULT_UPSTREAMS = {
    "openai": "https://api.openai.com",
    "anthropic": "https://api.anthropic.com",
}


def default_config_dir(environment: dict[str, str] | None = None) -> Path:
    env = environment if environment is not None else os.environ
    if env.get("APASTRA_CONFIG_DIR"):
        return Path(env["APASTRA_CONFIG_DIR"]).expanduser()
    if sys.platform == "win32" and env.get("APPDATA"):
        return Path(env["APPDATA"]) / "Apastra"
    if sys.platform == "darwin":
        return Path.home() / "Library" / "Application Support" / "Apastra"
    if env.get("XDG_CONFIG_HOME"):
        return Path(env["XDG_CONFIG_HOME"]) / "apastra"
    return Path.home() / ".config" / "apastra"


def default_log_dir(environment: dict[str, str] | None = None) -> Path:
    env = environment if environment is not None else os.environ
    if env.get("APASTRA_LOG_DIR"):
        return Path(env["APASTRA_LOG_DIR"]).expanduser()
    if sys.platform == "win32" and env.get("LOCALAPPDATA"):
        return Path(env["LOCALAPPDATA"]) / "Apastra" / "request-logs"
    if sys.platform == "darwin":
        return Path.home() / "Library" / "Application Support" / "Apastra" / "request-logs"
    if env.get("XDG_STATE_HOME"):
        return Path(env["XDG_STATE_HOME"]) / "apastra" / "request-logs"
    return Path.home() / ".local" / "state" / "apastra" / "request-logs"


@dataclass
class RequestLogConfig:
    enabled: bool = False
    adapters: dict[str, list[str]] = field(default_factory=dict)
    save_dir: Path = field(default_factory=default_log_dir)
    activation_mode: str = "session"
    retention_days: int = DEFAULT_RETENTION_DAYS
    max_bytes: int = DEFAULT_MAX_BYTES
    bind_host: str = "127.0.0.1"
    bind_port: int = DEFAULT_PORT
    upstreams: dict[str, str] = field(default_factory=lambda: dict(DEFAULT_UPSTREAMS))
    indefinite_retention_confirmed: bool = False
    schema_version: int = SCHEMA_VERSION

    @classmethod
    def default(cls) -> "RequestLogConfig":
        return cls()

    def normalized(self) -> "RequestLogConfig":
        adapters = {
            adapter: list(dict.fromkeys(providers))
            for adapter, providers in self.adapters.items()
        }
        return replace(
            self,
            save_dir=self.save_dir.expanduser().resolve(),
            adapters=adapters,
            upstreams=dict(self.upstreams),
        )

    def validate(self) -> None:
        if self.schema_version != SCHEMA_VERSION:
            raise ValueError(f"Unsupported request-log schema version: {self.schema_version}")
        try:
            if not ipaddress.ip_address(self.bind_host).is_loopback:
                raise ValueError("Request logging must bind to a loopback address")
        except ValueError as exc:
            if "loopback" in str(exc):
                raise
            raise ValueError("Request logging must bind to a numeric loopback address") from exc
        if not 0 <= self.bind_port <= 65535:
            raise ValueError("Gateway port must be between 0 and 65535")
        if self.activation_mode not in {"session", "persistent"}:
            raise ValueError("Activation mode must be 'session' or 'persistent'")
        if self.enabled and not self.adapters:
            raise ValueError("Enabled request logging requires at least one adapter")
        if self.retention_days < 0 or self.max_bytes < 0:
            raise ValueError("Retention values cannot be negative")
        if (self.retention_days == 0 or self.max_bytes == 0) and not self.indefinite_retention_confirmed:
            raise ValueError("indefinite retention requires explicit confirmation")
        for adapter, providers in self.adapters.items():
            if adapter not in SUPPORTED_ADAPTERS:
                raise ValueError(f"Unknown request-log adapter: {adapter}")
            if not providers:
                raise ValueError(f"Adapter {adapter} must select at least one provider")
            for provider in providers:
                if provider not in SUPPORTED_ADAPTERS[adapter]:
                    raise ValueError(f"Adapter {adapter} does not support provider {provider}")
        for provider in SUPPORTED_PROVIDERS:
            origin = self.upstreams.get(provider)
            if not origin:
                raise ValueError(f"Missing upstream origin for {provider}")
            parsed = urlsplit(origin)
            try:
                parsed.port
            except ValueError as exc:
                raise ValueError(f"Upstream for {provider} must be an HTTP(S) origin") from exc
            if (
                parsed.scheme not in {"http", "https"}
                or not parsed.hostname
                or parsed.username is not None
                or parsed.password is not None
                or parsed.path not in {"", "/"}
                or parsed.query
                or parsed.fragment
            ):
                raise ValueError(f"Upstream for {provider} must be an HTTP(S) origin")

    def to_dict(self) -> dict[str, Any]:
        config = self.normalized()
        config.validate()
        data = asdict(config)
        data["save_dir"] = str(config.save_dir)
        return data

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "RequestLogConfig":
        values = dict(data)
        known_fields = {item.name for item in fields(cls)}
        unknown_fields = sorted(set(values) - known_fields)
        if unknown_fields:
            raise ValueError(f"Unknown request-log configuration field: {', '.join(unknown_fields)}")
        try:
            values["save_dir"] = Path(values.get("save_dir") or default_log_dir())
            config = cls(**values).normalized()
            config.validate()
        except (AttributeError, TypeError) as exc:
            raise ValueError(f"Invalid request-log configuration: {exc}") from exc
        return config


class ConfigStore:
    def __init__(self, root: Path | str | None = None, environment: dict[str, str] | None = None):
        self.root = Path(root) if root is not None else default_config_dir(environment)
        self.root = self.root.expanduser().resolve()
        self.path = self.root / "request-log.json"

    def load(self) -> RequestLogConfig:
        if not self.path.exists():
            return RequestLogConfig.default().normalized()
        try:
            data = json.loads(self.path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            raise ValueError(f"Could not read request-log configuration: {exc}") from exc
        if not isinstance(data, dict):
            raise ValueError("Request-log configuration must be a JSON object")
        return RequestLogConfig.from_dict(data)

    def save(self, config: RequestLogConfig) -> RequestLogConfig:
        normalized = config.normalized()
        payload = json.dumps(normalized.to_dict(), indent=2, sort_keys=True).encode("utf-8") + b"\n"
        self.root.mkdir(parents=True, exist_ok=True, mode=0o700)
        _chmod_private(self.root, directory=True)
        temp_path = self.root / f".{self.path.name}.{os.getpid()}.tmp"
        _write_private(temp_path, payload)
        os.replace(temp_path, self.path)
        _chmod_private(self.path, directory=False)
        return normalized


def _write_private(path: Path, data: bytes) -> None:
    descriptor = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o600)
    try:
        with os.fdopen(descriptor, "wb") as handle:
            handle.write(data)
            handle.flush()
            os.fsync(handle.fileno())
    except Exception:
        try:
            path.unlink()
        except OSError:
            pass
        raise


def _chmod_private(path: Path, directory: bool) -> None:
    try:
        path.chmod(0o700 if directory else 0o600)
    except OSError:
        if os.name != "nt":
            raise
