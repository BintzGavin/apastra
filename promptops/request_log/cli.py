from __future__ import annotations

import argparse
import difflib
import json
import os
import signal
import subprocess
import sys
import time
import urllib.error
import urllib.request
from dataclasses import replace
from pathlib import Path
from typing import Callable, TextIO

from .adapters import (
    ManagedConfigInstall,
    build_session_launch,
    persistent_config_bytes,
)
from .artifacts import RequestArtifactStore
from .config import (
    DEFAULT_MAX_BYTES,
    DEFAULT_PORT,
    DEFAULT_RETENTION_DAYS,
    SUPPORTED_ADAPTERS,
    ConfigStore,
    RequestLogConfig,
    _chmod_private,
    _write_private,
    default_log_dir,
)
from .gateway import GatewayServer, format_gateway_origin


_BACKGROUND_PROCESSES: dict[int, subprocess.Popen] = {}


def main(
    argv: list[str] | None = None,
    *,
    input_fn: Callable[[str], str] = input,
    stdout: TextIO = sys.stdout,
    stderr: TextIO = sys.stderr,
    environment: dict[str, str] | None = None,
) -> int:
    args = _parser().parse_args(argv)
    env = dict(os.environ if environment is None else environment)
    store = ConfigStore(args.config_dir, environment=env)
    try:
        if args.command in {"configure", "onboard", "enable"}:
            return _configure(args, store, input_fn, stdout, stderr)
        if args.command == "status":
            return _status(args, store, stdout)
        if args.command == "serve":
            return _serve(store, stderr)
        if args.command == "start":
            return _start(store, stdout, stderr, env)
        if args.command == "stop":
            return _stop(store, stdout, stderr)
        if args.command == "run":
            return _run(args, store, stdout, stderr, env)
        if args.command == "install":
            return _install(args, store, stdout, stderr, env)
        if args.command == "disable":
            return _disable(args, store, stdout, stderr, env)
        if args.command == "list":
            return _list(args, store, stdout)
        if args.command == "show":
            return _show(args, store, stdout)
        if args.command == "prune":
            return _prune(args, store, stdout)
    except (ValueError, KeyError, RuntimeError, OSError) as exc:
        print(f"Error: {exc}", file=stderr)
        return 2
    return 2


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="apastra request-log", description="Opt-in local provider request logging"
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    configure = subparsers.add_parser(
        "configure", aliases=["onboard", "enable"], help="Configure request logging"
    )
    _config_dir_argument(configure)
    configure.add_argument(
        "--yes",
        action="store_true",
        help="Explicitly accept storage of complete request bodies",
    )
    configure.add_argument(
        "--adapters", help="Comma-separated adapter:provider selections"
    )
    configure.add_argument("--save-dir")
    configure.add_argument("--mode", choices=["session", "persistent"])
    configure.add_argument("--retention-days", type=int)
    configure.add_argument("--max-mb", type=int)
    configure.add_argument("--port", type=int)
    configure.add_argument("--indefinite-retention", action="store_true")

    status = subparsers.add_parser("status", help="Show request-log status")
    _config_dir_argument(status)
    status.add_argument("--json", action="store_true")

    for name, help_text in (
        ("serve", "Run the local logging gateway"),
        ("start", "Start the gateway in the background"),
        ("stop", "Stop the background gateway"),
    ):
        command = subparsers.add_parser(name, help=help_text)
        _config_dir_argument(command)

    run = subparsers.add_parser(
        "run", help="Launch an agent through a session-only gateway"
    )
    _config_dir_argument(run)
    run.add_argument("adapter", choices=sorted(SUPPORTED_ADAPTERS))
    run.add_argument("--provider", action="append", choices=["openai", "anthropic"])
    run.add_argument("agent_args", nargs="*")

    install = subparsers.add_parser(
        "install", help="Persistently route an adapter through the gateway"
    )
    _config_dir_argument(install)
    install.add_argument("adapter", choices=sorted(SUPPORTED_ADAPTERS))
    install.add_argument("--provider", action="append", choices=["openai", "anthropic"])
    install.add_argument("--dry-run", action="store_true")

    disable = subparsers.add_parser(
        "disable", help="Disable one adapter or all request logging"
    )
    _config_dir_argument(disable)
    disable.add_argument("adapter", nargs="?", choices=sorted(SUPPORTED_ADAPTERS))

    list_command = subparsers.add_parser("list", help="List captured provider requests")
    _config_dir_argument(list_command)
    list_command.add_argument("--json", action="store_true")

    show = subparsers.add_parser("show", help="Show one captured request")
    _config_dir_argument(show)
    show.add_argument("request_id")
    show.add_argument("--json", action="store_true")

    prune = subparsers.add_parser("prune", help="Apply request-log retention now")
    _config_dir_argument(prune)
    prune.add_argument("--json", action="store_true")
    return parser


def _config_dir_argument(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--config-dir", type=Path)


def _configure(
    args, store: ConfigStore, input_fn, stdout: TextIO, stderr: TextIO
) -> int:
    existing = store.load()
    installed = _installed_adapters(store)
    if installed:
        raise RuntimeError(
            "disable persistent request logging before reconfiguring; installed adapters: "
            + ", ".join(installed)
        )
    if _gateway_healthy(existing):
        raise RuntimeError("stop the request-log gateway before reconfiguring")
    print(
        "Request logging stores complete model request bodies, which may include private code, prompts, documents, and conversation history. Authentication headers are never stored.",
        file=stdout,
    )
    if not args.yes:
        answer = (
            input_fn(
                "Enable complete provider request logging? Type 'yes' to continue [y/N]: "
            )
            .strip()
            .lower()
        )
        if answer != "yes":
            if existing.enabled:
                print(
                    "Request logging remains enabled with its existing configuration; use 'disable' to turn it off.",
                    file=stdout,
                )
            else:
                print(
                    "Request logging remains disabled; no agent configuration was changed.",
                    file=stdout,
                )
            return 0

    adapters_text = args.adapters
    if not adapters_text:
        if args.yes:
            raise ValueError("--adapters is required with --yes")
        adapters_text = input_fn(
            "Adapters (for example codex:openai,claude-code:anthropic,opencode:openai+anthropic,pi:openai+anthropic): "
        ).strip()
    adapters = _parse_adapters(adapters_text)
    if args.yes and not args.save_dir:
        raise ValueError("--save-dir is required with --yes")
    save_text = (
        args.save_dir
        or input_fn(f"Save directory [{default_log_dir()}]: ").strip()
        or str(default_log_dir())
    )
    mode = args.mode or (
        "session"
        if args.yes
        else input_fn("Activation mode (session/persistent) [session]: ").strip()
        or "session"
    )
    retention_days = args.retention_days
    if retention_days is None:
        if args.yes:
            retention_days = DEFAULT_RETENTION_DAYS
        else:
            value = input_fn(f"Retention days [{DEFAULT_RETENTION_DAYS}]: ").strip()
            retention_days = int(value) if value else DEFAULT_RETENTION_DAYS
    max_mb = args.max_mb
    if max_mb is None:
        if args.yes:
            max_mb = DEFAULT_MAX_BYTES // (1024 * 1024)
        else:
            value = input_fn("Maximum retained MB [250]: ").strip()
            max_mb = int(value) if value else 250
    indefinite = args.indefinite_retention
    if retention_days == 0 or max_mb == 0:
        if not indefinite:
            if args.yes:
                raise ValueError(
                    "--indefinite-retention is required when a retention limit is zero with --yes"
                )
            answer = (
                input_fn(
                    "This creates indefinite retention. Type 'keep forever' to confirm: "
                )
                .strip()
                .lower()
            )
            indefinite = answer == "keep forever"

    config = RequestLogConfig(
        enabled=True,
        adapters=adapters,
        save_dir=Path(save_text),
        activation_mode=mode,
        retention_days=retention_days,
        max_bytes=max_mb * 1024 * 1024,
        bind_port=args.port if args.port is not None else DEFAULT_PORT,
        indefinite_retention_confirmed=indefinite,
    ).normalized()
    config.validate()
    config.save_dir.mkdir(parents=True, exist_ok=True, mode=0o700)
    _exclude_from_git(config.save_dir)
    _chmod_private(config.save_dir, directory=True)
    store.save(config)
    print("Request logging enabled.", file=stdout)
    print(f"Save directory: {config.save_dir}", file=stdout)
    print(f"Adapters: {_format_adapters(config.adapters)}", file=stdout)
    print(
        f"Retention: {config.retention_days or 'unlimited'} days / {_format_bytes(config.max_bytes)}",
        file=stdout,
    )
    first = next(iter(config.adapters))
    if config.activation_mode == "session":
        print(f"Next: apastra request-log run {first} --", file=stdout)
    else:
        print(f"Next: apastra request-log install {first}", file=stdout)
    return 0


def _status(args, store: ConfigStore, stdout: TextIO) -> int:
    config = store.load()
    payload = {
        "enabled": config.enabled,
        "config_dir": str(store.root),
        "adapters": config.adapters,
        "save_dir": str(config.save_dir),
        "activation_mode": config.activation_mode,
        "retention_days": config.retention_days,
        "max_bytes": config.max_bytes,
        "gateway_url": format_gateway_origin(config.bind_host, config.bind_port),
        "gateway_running": _gateway_healthy(config),
        "persistent_installs": _installed_adapters(store),
        "generic_environment": _generic_environment(store),
    }
    if args.json:
        print(json.dumps(payload, indent=2, sort_keys=True), file=stdout)
    else:
        print(
            f"Request logging: {'enabled' if config.enabled else 'disabled'}",
            file=stdout,
        )
        print(
            f"Gateway: {'running' if payload['gateway_running'] else 'stopped'}",
            file=stdout,
        )
        print(
            f"Adapters: {_format_adapters(config.adapters) if config.adapters else 'none'}",
            file=stdout,
        )
        print(f"Config directory: {store.root}", file=stdout)
        print(f"Save directory: {config.save_dir}", file=stdout)
        print(
            f"Retention: {config.retention_days or 'unlimited'} days / {_format_bytes(config.max_bytes)}",
            file=stdout,
        )
    return 0


def _serve(store: ConfigStore, stderr: TextIO) -> int:
    config = store.load()
    if not config.enabled:
        raise RuntimeError(
            "Request logging is disabled; run 'apastra request-log configure' first"
        )
    gateway = GatewayServer(config, RequestArtifactStore(config.save_dir))
    print(
        f"Apastra request logger listening on {format_gateway_origin(config.bind_host, config.bind_port)}",
        file=stderr,
    )
    try:
        gateway.serve_forever()
    except KeyboardInterrupt:
        return 130
    finally:
        gateway.shutdown()
    return 0


def _start(
    store: ConfigStore, stdout: TextIO, stderr: TextIO, environment: dict[str, str]
) -> int:
    config = store.load()
    if not config.enabled:
        raise RuntimeError("Request logging is disabled")
    if config.bind_port == 0:
        raise ValueError("Persistent gateway requires a non-zero configured port")
    if _gateway_healthy(config):
        print("Request-log gateway is already running.", file=stdout)
        return 0
    store.root.mkdir(parents=True, exist_ok=True, mode=0o700)
    log_path = store.root / "gateway.log"
    log_handle = os.open(log_path, os.O_WRONLY | os.O_CREAT | os.O_APPEND, 0o600)
    module_name = __package__ + ".cli"
    import_root = Path(__file__).resolve().parents[2]
    child_environment = dict(environment)
    existing_pythonpath = child_environment.get("PYTHONPATH")
    child_environment["PYTHONPATH"] = str(import_root) + (
        os.pathsep + existing_pythonpath if existing_pythonpath else ""
    )
    command = [
        sys.executable,
        "-m",
        module_name,
        "serve",
        "--config-dir",
        str(store.root),
    ]
    kwargs = {
        "env": child_environment,
        "stdin": subprocess.DEVNULL,
        "stdout": log_handle,
        "stderr": log_handle,
        "close_fds": True,
    }
    if os.name == "nt":
        kwargs["creationflags"] = (
            subprocess.CREATE_NEW_PROCESS_GROUP | subprocess.DETACHED_PROCESS
        )
    else:
        kwargs["start_new_session"] = True
    try:
        process = subprocess.Popen(command, **kwargs)
    finally:
        os.close(log_handle)
    _BACKGROUND_PROCESSES[process.pid] = process
    pid_path = store.root / "gateway.pid"
    try:
        _write_private(pid_path, f"{process.pid}\n".encode("ascii"))
        for _ in range(40):
            if _gateway_healthy(config):
                print(f"Request-log gateway started (PID {process.pid}).", file=stdout)
                return 0
            if process.poll() is not None:
                break
            time.sleep(0.05)
    except BaseException:
        _terminate_process(process)
        _BACKGROUND_PROCESSES.pop(process.pid, None)
        pid_path.unlink(missing_ok=True)
        raise
    _terminate_process(process)
    _BACKGROUND_PROCESSES.pop(process.pid, None)
    pid_path.unlink(missing_ok=True)
    print(f"Gateway did not become ready; see {log_path}", file=stderr)
    return 1


def _terminate_process(process: subprocess.Popen) -> None:
    if process.poll() is not None:
        return
    process.terminate()
    try:
        process.wait(timeout=5)
    except subprocess.TimeoutExpired:
        process.kill()
        process.wait(timeout=5)


def _stop(store: ConfigStore, stdout: TextIO, stderr: TextIO) -> int:
    pid_path = store.root / "gateway.pid"
    if not pid_path.exists():
        print("Request-log gateway is not running.", file=stdout)
        return 0
    try:
        pid = int(pid_path.read_text().strip())
        health = _gateway_health(store.load())
        if not health or health.get("pid") != pid:
            pid_path.unlink(missing_ok=True)
            print(
                "Removed stale request-log gateway state; no process was terminated.",
                file=stdout,
            )
            return 0
        os.kill(pid, signal.SIGTERM)
        process = _BACKGROUND_PROCESSES.pop(pid, None)
        if process is not None:
            try:
                process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                pass
    except (ValueError, ProcessLookupError):
        pass
    except PermissionError as exc:
        print(f"Could not stop gateway: {exc}", file=stderr)
        return 1
    pid_path.unlink(missing_ok=True)
    print("Request-log gateway stopped.", file=stdout)
    return 0


def _run(
    args,
    store: ConfigStore,
    stdout: TextIO,
    stderr: TextIO,
    environment: dict[str, str],
) -> int:
    config = store.load()
    if not config.enabled:
        raise RuntimeError("Request logging is disabled")
    if args.adapter not in config.adapters:
        raise ValueError(f"Adapter {args.adapter} is not enabled")
    providers = args.provider or config.adapters[args.adapter]
    if not set(providers).issubset(config.adapters[args.adapter]):
        raise ValueError("Requested provider is not enabled for this adapter")
    session_config = replace(config, bind_port=0)
    agent_args = list(args.agent_args)
    if agent_args and agent_args[0] == "--":
        agent_args.pop(0)
    with GatewayServer(
        session_config, RequestArtifactStore(config.save_dir)
    ) as gateway:
        launch = build_session_launch(
            args.adapter,
            agent_args,
            gateway.base_url,
            providers,
            parent_environment=environment,
        )
        child_environment = dict(environment)
        child_environment.update(launch.environment)
        print(
            f"Request logging active at {gateway.base_url}; logs: {config.save_dir}",
            file=stderr,
        )
        try:
            result = subprocess.run(launch.command, env=child_environment, check=False)
            return result.returncode
        except FileNotFoundError as exc:
            raise RuntimeError(
                f"Could not launch {launch.command[0]}: command not found"
            ) from exc
        finally:
            launch.cleanup()


def _install(
    args,
    store: ConfigStore,
    stdout: TextIO,
    stderr: TextIO,
    environment: dict[str, str],
) -> int:
    config = store.load()
    if not config.enabled:
        raise RuntimeError("Request logging is disabled")
    if args.adapter not in config.adapters:
        raise ValueError(f"Adapter {args.adapter} is not enabled")
    providers = args.provider or config.adapters[args.adapter]
    if not set(providers).issubset(config.adapters[args.adapter]):
        raise ValueError("Requested provider is not enabled for this adapter")
    target = _adapter_target(args.adapter, store, environment)
    original = (
        target.read_bytes()
        if target.exists()
        else (b"" if args.adapter == "codex" else b"{}\n")
    )
    gateway = format_gateway_origin(config.bind_host, config.bind_port)
    applied = persistent_config_bytes(args.adapter, original, gateway, providers)
    print(f"Target: {target}", file=stdout)
    before = original.decode("utf-8", errors="replace").splitlines(keepends=True)
    after = applied.decode("utf-8", errors="replace").splitlines(keepends=True)
    print("Proposed change:", file=stdout)
    print(
        "".join(
            difflib.unified_diff(
                before, after, fromfile=str(target), tofile=str(target) + " (proposed)"
            )
        ),
        file=stdout,
    )
    if args.dry_run:
        return 0
    install = ManagedConfigInstall(store.root / "installs", args.adapter, target)
    previous_mode = config.activation_mode
    was_committed = install.apply(applied)
    try:
        config.activation_mode = "persistent"
        store.save(config)
    except BaseException:
        if not was_committed:
            install.restore()
            config.activation_mode = previous_mode
            store.save(config)
        raise
    gateway_started = False
    try:
        gateway_was_running = _gateway_healthy(config)
        result = _start(store, stdout, stderr, environment)
        gateway_started = result == 0 and not gateway_was_running
        if result == 0:
            install.commit()
    except BaseException:
        if not was_committed:
            if gateway_started:
                _stop(store, stdout, stderr)
            install.restore()
            config.activation_mode = previous_mode
            store.save(config)
        raise
    if result == 0:
        print(f"Persistent request logging installed for {args.adapter}.", file=stdout)
    elif not was_committed:
        install.restore()
        config.activation_mode = previous_mode
        store.save(config)
        print(
            f"Persistent change for {args.adapter} was rolled back because the gateway did not start.",
            file=stderr,
        )
    return result


def _disable(
    args,
    store: ConfigStore,
    stdout: TextIO,
    stderr: TextIO,
    environment: dict[str, str],
) -> int:
    config = store.load()
    adapters = (
        [args.adapter]
        if args.adapter
        else list(dict.fromkeys([*config.adapters, *_installed_adapters(store)]))
    )
    installs = []
    for adapter in adapters:
        state_root = store.root / "installs"
        manifest_path = state_root / adapter / "install.json"
        if manifest_path.exists():
            install = ManagedConfigInstall.from_state(state_root, adapter)
        else:
            target = _adapter_target(adapter, store, environment)
            install = ManagedConfigInstall(state_root, adapter, target)
        install.ensure_restorable()
        installs.append((adapter, install))
    for adapter, install in installs:
        install.restore()
        config.adapters.pop(adapter, None)
        print(f"Disabled request logging for {adapter}.", file=stdout)
    if not config.adapters:
        config.enabled = False
        _stop(store, stdout, stderr)
    store.save(config)
    return 0


def _list(args, store: ConfigStore, stdout: TextIO) -> int:
    config = store.load()
    rows = RequestArtifactStore(config.save_dir).list_requests()
    if args.json:
        print(json.dumps(rows, indent=2, sort_keys=True), file=stdout)
    elif not rows:
        print("No captured requests.", file=stdout)
    else:
        for row in rows:
            print(
                f"{row['request_id']}  {row['timestamp']}  {row['provider']}/{row['adapter']}  {row.get('model') or '-'}  {row['body_bytes']} bytes  {row.get('response_status') or row.get('error_class') or 'pending'}",
                file=stdout,
            )
    return 0


def _show(args, store: ConfigStore, stdout: TextIO) -> int:
    config = store.load()
    shown = RequestArtifactStore(config.save_dir).show_request(args.request_id)
    payload = {"metadata": shown["metadata"], "body": shown["body"]}
    if args.json:
        print(
            json.dumps(payload, indent=2, sort_keys=True, ensure_ascii=False),
            file=stdout,
        )
    else:
        print(json.dumps(payload["metadata"], indent=2, sort_keys=True), file=stdout)
        print("\nRequest body:\n", file=stdout)
        if isinstance(payload["body"], (dict, list)):
            print(
                json.dumps(payload["body"], indent=2, ensure_ascii=False), file=stdout
            )
        else:
            print(payload["body"], file=stdout)
    return 0


def _prune(args, store: ConfigStore, stdout: TextIO) -> int:
    config = store.load()
    removed = RequestArtifactStore(config.save_dir).prune(
        config.retention_days, config.max_bytes
    )
    payload = {"removed": removed}
    if args.json:
        print(json.dumps(payload, indent=2), file=stdout)
    else:
        print(f"Removed {len(removed)} request log(s).", file=stdout)
    return 0


def _parse_adapters(text: str) -> dict[str, list[str]]:
    if not text.strip():
        raise ValueError("Select at least one adapter")
    result: dict[str, list[str]] = {}
    for selection in text.split(","):
        if ":" not in selection:
            raise ValueError(
                f"Adapter selection must use adapter:provider syntax: {selection}"
            )
        adapter, provider_text = (part.strip() for part in selection.split(":", 1))
        providers = [part.strip() for part in provider_text.split("+") if part.strip()]
        if adapter not in SUPPORTED_ADAPTERS:
            raise ValueError(f"Unknown adapter: {adapter}")
        unsupported = set(providers) - SUPPORTED_ADAPTERS[adapter]
        if not providers or unsupported:
            raise ValueError(f"Invalid providers for {adapter}: {provider_text}")
        result[adapter] = list(dict.fromkeys(providers))
    return result


def _adapter_target(
    adapter: str, store: ConfigStore, environment: dict[str, str]
) -> Path:
    if adapter == "codex":
        root = (
            environment.get("APASTRA_CODEX_HOME")
            or environment.get("CODEX_HOME")
            or Path.home() / ".codex"
        )
        return Path(root).expanduser() / "config.toml"
    if adapter == "claude-code":
        root = (
            environment.get("APASTRA_CLAUDE_HOME")
            or environment.get("CLAUDE_CONFIG_DIR")
            or Path.home() / ".claude"
        )
        return Path(root).expanduser() / "settings.json"
    if adapter == "opencode":
        explicit = environment.get("APASTRA_OPENCODE_CONFIG") or environment.get(
            "OPENCODE_CONFIG"
        )
        if explicit:
            return Path(explicit).expanduser()
        root = Path(environment.get("XDG_CONFIG_HOME", Path.home() / ".config"))
        config_root = root.expanduser() / "opencode"
        jsonc_path = config_root / "opencode.jsonc"
        return jsonc_path if jsonc_path.exists() else config_root / "opencode.json"
    if adapter == "pi":
        return (
            Path(
                environment.get("PI_CODING_AGENT_DIR", Path.home() / ".pi" / "agent")
            ).expanduser()
            / "models.json"
        )
    if adapter == "generic":
        return store.root / "generic-provider-env.json"
    raise ValueError(f"Unknown adapter: {adapter}")


def _exclude_from_git(save_dir: Path) -> None:
    try:
        root_result = subprocess.run(
            ["git", "-C", str(save_dir), "rev-parse", "--show-toplevel"],
            text=True,
            capture_output=True,
            timeout=5,
            check=False,
        )
    except (OSError, subprocess.SubprocessError):
        return
    if root_result.returncode != 0:
        return
    git_root = Path(root_result.stdout.strip()).resolve()
    try:
        relative = save_dir.resolve().relative_to(git_root)
    except ValueError:
        return
    if relative == Path("."):
        raise ValueError(
            "Choose a dedicated subdirectory inside the Git worktree for request logs"
        )
    exclude_result = subprocess.run(
        ["git", "-C", str(git_root), "rev-parse", "--git-path", "info/exclude"],
        text=True,
        capture_output=True,
        timeout=5,
        check=False,
    )
    if exclude_result.returncode != 0:
        return
    exclude = Path(exclude_result.stdout.strip())
    if not exclude.is_absolute():
        exclude = git_root / exclude
    exclude.parent.mkdir(parents=True, exist_ok=True)
    relative_text = relative.as_posix().rstrip("/")
    if "\n" in relative_text or "\r" in relative_text:
        raise ValueError("Git worktree request-log paths cannot contain newlines")
    escaped_relative = "".join(
        "\\" + character if character in {"\\", "*", "?", "["} else character
        for character in relative_text
    )
    line = "/" + escaped_relative + "/"
    existing = exclude.read_text(encoding="utf-8") if exclude.exists() else ""
    if line not in existing.splitlines():
        with exclude.open("a", encoding="utf-8") as handle:
            if existing and not existing.endswith("\n"):
                handle.write("\n")
            handle.write(
                "# Apastra provider request logs (local opt-in)\n" + line + "\n"
            )


def _gateway_healthy(config: RequestLogConfig) -> bool:
    return _gateway_health(config) is not None


def _gateway_health(config: RequestLogConfig) -> dict | None:
    if not config.enabled or not config.bind_port:
        return None
    try:
        origin = format_gateway_origin(config.bind_host, config.bind_port)
        with urllib.request.urlopen(f"{origin}/health", timeout=0.15) as response:
            payload = json.loads(response.read())
            if (
                response.status == 200
                and isinstance(payload, dict)
                and payload.get("status") == "ok"
                and payload.get("save_dir") == str(config.save_dir)
            ):
                return payload
    except (OSError, urllib.error.URLError, json.JSONDecodeError):
        pass
    return None


def _installed_adapters(store: ConfigStore) -> list[str]:
    root = store.root / "installs"
    if not root.exists():
        return []
    return sorted(path.parent.name for path in root.glob("*/install.json"))


def _generic_environment(store: ConfigStore) -> dict[str, str]:
    if "generic" not in _installed_adapters(store):
        return {}
    path = store.root / "generic-provider-env.json"
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return {}
    environment = payload.get("environment") if isinstance(payload, dict) else None
    if not isinstance(environment, dict):
        return {}
    return {
        key: value
        for key, value in environment.items()
        if isinstance(key, str) and isinstance(value, str)
    }


def _format_adapters(adapters: dict[str, list[str]]) -> str:
    return ", ".join(
        f"{adapter}:{'+'.join(providers)}" for adapter, providers in adapters.items()
    )


def _format_bytes(value: int) -> str:
    return "unlimited" if value == 0 else f"{value / (1024 * 1024):g} MB"


if __name__ == "__main__":
    raise SystemExit(main())
