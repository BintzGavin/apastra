import io
import json
import os
import stat
import subprocess
import socket
import tempfile
import time
import unittest
from pathlib import Path
from unittest import mock

from promptops.request_log.adapters import (
    ManagedConfigInstall,
    persistent_config_bytes,
)
from promptops.request_log import cli as request_log_cli
from promptops.request_log.cli import main
from promptops.request_log.config import ConfigStore, RequestLogConfig
from tests.test_request_log_gateway import FakeProvider, FakeProviderHandler


FAKE_AGENT = r"""#!/usr/bin/env python3
import json
import os
import sys
import urllib.request
from pathlib import Path

name = Path(sys.argv[0]).name
routes = []
if name == "codex":
    value = next(arg for arg in sys.argv if arg.startswith("openai_base_url="))
    routes.append(("openai", value.split("=", 1)[1].strip('"') + "/responses"))
elif name == "claude":
    routes.append(("anthropic", os.environ["ANTHROPIC_BASE_URL"] + "/v1/messages"))
elif name == "opencode":
    config = json.loads(os.environ["OPENCODE_CONFIG_CONTENT"])
    for provider in ("openai", "anthropic"):
        base = config["provider"][provider]["options"]["baseURL"]
        routes.append((provider, base + ("/responses" if provider == "openai" else "/messages")))
elif name == "pi":
    config = json.loads((Path(os.environ["PI_CODING_AGENT_DIR"]) / "models.json").read_text())
    for provider in ("openai", "anthropic"):
        base = config["providers"][provider]["baseUrl"]
        routes.append((provider, base + ("/responses" if provider == "openai" else "/messages")))
else:
    routes.append(("openai", os.environ["OPENAI_BASE_URL"] + "/responses"))
    routes.append(("anthropic", os.environ["ANTHROPIC_BASE_URL"] + "/v1/messages"))

for provider, url in routes:
    body = json.dumps({"model": name + "-" + provider, "messages": [{"role": "user", "content": "hello"}]}, separators=(",", ":")).encode()
    request = urllib.request.Request(
        url,
        data=body,
        headers={"Content-Type": "application/json", "Authorization": "Bearer subprocess-secret"},
        method="POST",
    )
    with urllib.request.urlopen(request, timeout=5) as response:
        response.read()
"""


class AdapterEndToEndTests(unittest.TestCase):
    def test_cli_run_routes_every_adapter_and_provider_through_gateway(self):
        with tempfile.TemporaryDirectory() as temp_dir, FakeProvider() as upstream:
            root = Path(temp_dir)
            bin_dir = root / "bin"
            bin_dir.mkdir()
            for command in ("codex", "claude", "opencode", "pi", "generic-agent"):
                path = bin_dir / command
                path.write_text(FAKE_AGENT)
                path.chmod(path.stat().st_mode | stat.S_IXUSR)
            pi_home = root / "pi-home"
            pi_home.mkdir()
            (pi_home / "auth.json").write_text('{"token":"preserved"}\n')
            config_store = ConfigStore(root / "config")
            config_store.save(
                RequestLogConfig(
                    enabled=True,
                    adapters={
                        "codex": ["openai"],
                        "claude-code": ["anthropic"],
                        "opencode": ["openai", "anthropic"],
                        "pi": ["openai", "anthropic"],
                        "generic": ["openai", "anthropic"],
                    },
                    save_dir=root / "logs",
                    bind_port=0,
                    upstreams={"openai": upstream.origin, "anthropic": upstream.origin},
                )
            )
            environment = {
                **os.environ,
                "PATH": str(bin_dir) + os.pathsep + os.environ.get("PATH", ""),
                "PI_CODING_AGENT_DIR": str(pi_home),
            }

            commands = [
                ["run", "--config-dir", str(config_store.root), "codex"],
                ["run", "--config-dir", str(config_store.root), "claude-code"],
                ["run", "--config-dir", str(config_store.root), "opencode"],
                ["run", "--config-dir", str(config_store.root), "pi"],
                [
                    "run",
                    "--config-dir",
                    str(config_store.root),
                    "generic",
                    "--",
                    "generic-agent",
                ],
            ]
            for command in commands:
                with self.subTest(command=command):
                    result = main(
                        command,
                        stdout=io.StringIO(),
                        stderr=io.StringIO(),
                        environment=environment,
                    )
                    self.assertEqual(result, 0)

            self.assertEqual(len(FakeProviderHandler.requests), 8)
            rows = (
                __import__(
                    "promptops.request_log.artifacts", fromlist=["RequestArtifactStore"]
                )
                .RequestArtifactStore(root / "logs")
                .list_requests()
            )
            self.assertEqual(len(rows), 8)
            pairs = {(row["adapter"], row["provider"]) for row in rows}
            self.assertEqual(
                pairs,
                {
                    ("codex", "openai"),
                    ("claude-code", "anthropic"),
                    ("opencode", "openai"),
                    ("opencode", "anthropic"),
                    ("pi", "openai"),
                    ("pi", "anthropic"),
                    ("generic", "openai"),
                    ("generic", "anthropic"),
                },
            )
            persisted = b"\n".join(
                path.read_bytes()
                for path in root.rglob("*")
                if path.is_file() and "bin" not in path.parts
            )
            self.assertNotIn(b"subprocess-secret", persisted)


class PersistentCliTests(unittest.TestCase):
    def test_start_terminates_child_when_readiness_wait_is_interrupted(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            store = ConfigStore(root / "config")
            store.save(
                RequestLogConfig(
                    enabled=True,
                    adapters={"generic": ["openai"]},
                    save_dir=root / "logs",
                    bind_port=65532,
                )
            )
            process = mock.Mock(pid=43209)
            process.poll.return_value = None
            process.wait.return_value = 0

            try:
                with (
                    mock.patch(
                        "promptops.request_log.cli.subprocess.Popen",
                        return_value=process,
                    ),
                    mock.patch(
                        "promptops.request_log.cli._gateway_healthy",
                        return_value=False,
                    ),
                    mock.patch(
                        "promptops.request_log.cli.time.sleep",
                        side_effect=KeyboardInterrupt,
                    ),
                    self.assertRaises(KeyboardInterrupt),
                ):
                    main(
                        ["start", "--config-dir", str(store.root)],
                        stdout=io.StringIO(),
                        stderr=io.StringIO(),
                    )

                process.terminate.assert_called_once_with()
                process.wait.assert_called_once_with(timeout=5)
                self.assertNotIn(process.pid, request_log_cli._BACKGROUND_PROCESSES)
                self.assertFalse((store.root / "gateway.pid").exists())
            finally:
                request_log_cli._BACKGROUND_PROCESSES.pop(process.pid, None)

    def test_start_terminates_child_if_pid_state_cannot_be_written(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            store = ConfigStore(root / "config")
            store.save(
                RequestLogConfig(
                    enabled=True,
                    adapters={"generic": ["openai"]},
                    save_dir=root / "logs",
                    bind_port=65533,
                )
            )
            process = mock.Mock(pid=43210)
            process.poll.return_value = None
            process.wait.return_value = 0
            stderr = io.StringIO()

            try:
                with (
                    mock.patch(
                        "promptops.request_log.cli.subprocess.Popen",
                        return_value=process,
                    ),
                    mock.patch(
                        "promptops.request_log.cli._write_private",
                        side_effect=OSError("disk full"),
                    ),
                ):
                    result = main(
                        ["start", "--config-dir", str(store.root)],
                        stdout=io.StringIO(),
                        stderr=stderr,
                    )

                self.assertEqual(result, 2)
                self.assertIn("disk full", stderr.getvalue())
                process.terminate.assert_called_once_with()
                process.wait.assert_called_once_with(timeout=5)
                self.assertNotIn(process.pid, request_log_cli._BACKGROUND_PROCESSES)
                self.assertFalse((store.root / "gateway.pid").exists())
            finally:
                request_log_cli._BACKGROUND_PROCESSES.pop(process.pid, None)

    def test_background_gateway_start_status_and_stop(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            with socket.socket() as probe:
                probe.bind(("127.0.0.1", 0))
                port = probe.getsockname()[1]
            store = ConfigStore(root / "config")
            store.save(
                RequestLogConfig(
                    enabled=True,
                    adapters={"generic": ["openai"]},
                    save_dir=root / "logs",
                    bind_port=port,
                )
            )
            try:
                start_out = io.StringIO()
                self.assertEqual(
                    main(
                        ["start", "--config-dir", str(store.root)],
                        stdout=start_out,
                        stderr=io.StringIO(),
                    ),
                    0,
                )
                self.assertIn("started", start_out.getvalue())
                status_out = io.StringIO()
                self.assertEqual(
                    main(
                        ["status", "--config-dir", str(store.root), "--json"],
                        stdout=status_out,
                        stderr=io.StringIO(),
                    ),
                    0,
                )
                self.assertTrue(json.loads(status_out.getvalue())["gateway_running"])
                self.assertEqual(
                    main(
                        ["stop", "--config-dir", str(store.root)],
                        stdout=io.StringIO(),
                        stderr=io.StringIO(),
                    ),
                    0,
                )
                for _ in range(40):
                    status_out = io.StringIO()
                    main(
                        ["status", "--config-dir", str(store.root), "--json"],
                        stdout=status_out,
                        stderr=io.StringIO(),
                    )
                    if not json.loads(status_out.getvalue())["gateway_running"]:
                        break
                    time.sleep(0.05)
                self.assertFalse(json.loads(status_out.getvalue())["gateway_running"])
            finally:
                main(
                    ["stop", "--config-dir", str(store.root)],
                    stdout=io.StringIO(),
                    stderr=io.StringIO(),
                )

    def test_stop_removes_stale_pid_without_killing_any_process(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            store = ConfigStore(root / "config")
            store.save(
                RequestLogConfig(
                    enabled=True,
                    adapters={"generic": ["openai"]},
                    save_dir=root / "logs",
                    bind_port=65534,
                )
            )
            (store.root / "gateway.pid").write_text(str(os.getpid()))

            with mock.patch("promptops.request_log.cli.os.kill") as kill:
                output = io.StringIO()
                result = main(
                    ["stop", "--config-dir", str(store.root)],
                    stdout=output,
                    stderr=io.StringIO(),
                )

            self.assertEqual(result, 0)
            kill.assert_not_called()
            self.assertIn("stale", output.getvalue())

    def test_install_and_disable_all_adapters_restores_original_bytes(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            paths = {
                "codex": root / "codex" / "config.toml",
                "claude-code": root / "claude" / "settings.json",
                "opencode": root / "opencode" / "opencode.json",
                "pi": root / "pi" / "models.json",
            }
            originals = {
                "codex": b'model = "gpt-test"\n',
                "claude-code": b'{"permissions":{"allow":["Read"]}}\n',
                "opencode": b'{"theme":"dark"}\n',
                "pi": b'{"providers":{"anthropic":{"headers":{"x-existing":"yes"}}}}\n',
            }
            for adapter, path in paths.items():
                path.parent.mkdir(parents=True)
                path.write_bytes(originals[adapter])
            environment = {
                **os.environ,
                "APASTRA_CODEX_HOME": str(paths["codex"].parent),
                "APASTRA_CLAUDE_HOME": str(paths["claude-code"].parent),
                "APASTRA_OPENCODE_CONFIG": str(paths["opencode"]),
                "PI_CODING_AGENT_DIR": str(paths["pi"].parent),
            }
            store = ConfigStore(root / "config")
            store.save(
                RequestLogConfig(
                    enabled=True,
                    adapters={
                        "codex": ["openai"],
                        "claude-code": ["anthropic"],
                        "opencode": ["openai", "anthropic"],
                        "pi": ["openai", "anthropic"],
                        "generic": ["openai", "anthropic"],
                    },
                    save_dir=root / "logs",
                    bind_port=43123,
                )
            )

            with mock.patch("promptops.request_log.cli._start", return_value=0):
                for adapter in ("codex", "claude-code", "opencode", "pi", "generic"):
                    output = io.StringIO()
                    result = main(
                        ["install", "--config-dir", str(store.root), adapter],
                        stdout=output,
                        stderr=io.StringIO(),
                        environment=environment,
                    )
                    self.assertEqual(result, 0)
                    self.assertIn("Proposed change", output.getvalue())

            for adapter, path in paths.items():
                self.assertNotEqual(path.read_bytes(), originals[adapter])
            self.assertTrue((store.root / "generic-provider-env.json").exists())
            self.assertEqual(
                sorted(
                    path.parent.name
                    for path in (store.root / "installs").glob("*/install.json")
                ),
                ["claude-code", "codex", "generic", "opencode", "pi"],
            )
            status_out = io.StringIO()
            self.assertEqual(
                main(
                    ["status", "--config-dir", str(store.root), "--json"],
                    stdout=status_out,
                    stderr=io.StringIO(),
                    environment=environment,
                ),
                0,
            )
            generic_environment = json.loads(status_out.getvalue())[
                "generic_environment"
            ]
            self.assertEqual(
                generic_environment,
                {
                    "ANTHROPIC_BASE_URL": "http://127.0.0.1:43123/anthropic/generic",
                    "OPENAI_BASE_URL": "http://127.0.0.1:43123/openai/generic/v1",
                },
            )

            with mock.patch("promptops.request_log.cli._stop", return_value=0):
                result = main(
                    ["disable", "--config-dir", str(store.root)],
                    stdout=io.StringIO(),
                    stderr=io.StringIO(),
                    environment=environment,
                )
            self.assertEqual(result, 0)
            for adapter, path in paths.items():
                self.assertEqual(path.read_bytes(), originals[adapter])
            self.assertFalse((store.root / "generic-provider-env.json").exists())
            self.assertFalse(store.load().enabled)

    def test_failed_gateway_start_rolls_back_new_persistent_install(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            codex_home = root / "codex"
            codex_home.mkdir()
            target = codex_home / "config.toml"
            original = b'model = "gpt-test"\n'
            target.write_bytes(original)
            store = ConfigStore(root / "config")
            store.save(
                RequestLogConfig(
                    enabled=True,
                    adapters={"codex": ["openai"]},
                    save_dir=root / "logs",
                    activation_mode="session",
                )
            )
            environment = {**os.environ, "APASTRA_CODEX_HOME": str(codex_home)}

            with mock.patch("promptops.request_log.cli._start", return_value=1):
                result = main(
                    ["install", "--config-dir", str(store.root), "codex"],
                    stdout=io.StringIO(),
                    stderr=io.StringIO(),
                    environment=environment,
                )

            self.assertEqual(result, 1)
            self.assertEqual(target.read_bytes(), original)
            self.assertFalse(
                (store.root / "installs" / "codex" / "install.json").exists()
            )
            self.assertEqual(store.load().activation_mode, "session")

    def test_gateway_start_exception_rolls_back_new_persistent_install(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            codex_home = root / "codex"
            codex_home.mkdir()
            target = codex_home / "config.toml"
            original = b'model = "gpt-test"\n'
            target.write_bytes(original)
            store = ConfigStore(root / "config")
            store.save(
                RequestLogConfig(
                    enabled=True,
                    adapters={"codex": ["openai"]},
                    save_dir=root / "logs",
                    activation_mode="session",
                )
            )
            environment = {**os.environ, "APASTRA_CODEX_HOME": str(codex_home)}

            with mock.patch(
                "promptops.request_log.cli._start",
                side_effect=OSError("could not spawn gateway"),
            ):
                result = main(
                    ["install", "--config-dir", str(store.root), "codex"],
                    stdout=io.StringIO(),
                    stderr=io.StringIO(),
                    environment=environment,
                )

            self.assertEqual(result, 2)
            self.assertEqual(target.read_bytes(), original)
            self.assertFalse(
                (store.root / "installs" / "codex" / "install.json").exists()
            )
            self.assertEqual(store.load().activation_mode, "session")

    def test_partial_activation_mode_save_is_rolled_back(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            codex_home = root / "codex"
            codex_home.mkdir()
            target = codex_home / "config.toml"
            original = b'model = "gpt-test"\n'
            target.write_bytes(original)
            store = ConfigStore(root / "config")
            store.save(
                RequestLogConfig(
                    enabled=True,
                    adapters={"codex": ["openai"]},
                    save_dir=root / "logs",
                    activation_mode="session",
                )
            )
            real_save = ConfigStore.save
            calls = 0

            def fail_after_first_save(config_store, config):
                nonlocal calls
                calls += 1
                saved = real_save(config_store, config)
                if calls == 1:
                    raise OSError("simulated post-save failure")
                return saved

            stderr = io.StringIO()
            with mock.patch.object(ConfigStore, "save", new=fail_after_first_save):
                result = main(
                    ["install", "--config-dir", str(store.root), "codex"],
                    stdout=io.StringIO(),
                    stderr=stderr,
                    environment={**os.environ, "CODEX_HOME": str(codex_home)},
                )

            self.assertEqual(result, 2)
            self.assertIn("simulated post-save failure", stderr.getvalue())
            self.assertEqual(target.read_bytes(), original)
            self.assertFalse((store.root / "installs" / "codex").exists())
            self.assertEqual(store.load().activation_mode, "session")

    def test_failed_gateway_start_rolls_back_a_retried_prepared_install(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            codex_home = root / "codex"
            codex_home.mkdir()
            target = codex_home / "config.toml"
            original = b'model = "gpt-test"\n'
            target.write_bytes(original)
            store = ConfigStore(root / "config")
            store.save(
                RequestLogConfig(
                    enabled=True,
                    adapters={"codex": ["openai"]},
                    save_dir=root / "logs",
                    activation_mode="session",
                )
            )
            applied = persistent_config_bytes(
                "codex",
                original,
                "http://127.0.0.1:43123",
                ["openai"],
            )
            install = ManagedConfigInstall(
                store.root / "installs", "codex", target
            )
            install.apply(applied)
            target.write_bytes(original)

            with mock.patch("promptops.request_log.cli._start", return_value=1):
                result = main(
                    ["install", "--config-dir", str(store.root), "codex"],
                    stdout=io.StringIO(),
                    stderr=io.StringIO(),
                    environment={**os.environ, "CODEX_HOME": str(codex_home)},
                )

            self.assertEqual(result, 1)
            self.assertEqual(target.read_bytes(), original)
            self.assertFalse(install.root.exists())
            self.assertEqual(store.load().activation_mode, "session")

    def test_failed_gateway_start_rolls_back_an_interrupted_applied_install(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            codex_home = root / "codex"
            codex_home.mkdir()
            target = codex_home / "config.toml"
            original = b'model = "gpt-test"\n'
            target.write_bytes(original)
            store = ConfigStore(root / "config")
            store.save(
                RequestLogConfig(
                    enabled=True,
                    adapters={"codex": ["openai"]},
                    save_dir=root / "logs",
                    activation_mode="persistent",
                )
            )
            applied = persistent_config_bytes(
                "codex",
                original,
                "http://127.0.0.1:43123",
                ["openai"],
            )
            install = ManagedConfigInstall(
                store.root / "installs", "codex", target
            )
            install.apply(applied)

            with mock.patch("promptops.request_log.cli._start", return_value=1):
                result = main(
                    ["install", "--config-dir", str(store.root), "codex"],
                    stdout=io.StringIO(),
                    stderr=io.StringIO(),
                    environment={**os.environ, "CODEX_HOME": str(codex_home)},
                )

            self.assertEqual(result, 1)
            self.assertEqual(target.read_bytes(), original)
            self.assertFalse(install.root.exists())
            self.assertEqual(store.load().activation_mode, "persistent")

    def test_failed_restart_preserves_a_completed_persistent_install(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            codex_home = root / "codex"
            codex_home.mkdir()
            target = codex_home / "config.toml"
            original = b'model = "gpt-test"\n'
            target.write_bytes(original)
            store = ConfigStore(root / "config")
            store.save(
                RequestLogConfig(
                    enabled=True,
                    adapters={"codex": ["openai"]},
                    save_dir=root / "logs",
                    activation_mode="session",
                )
            )
            environment = {**os.environ, "CODEX_HOME": str(codex_home)}

            with mock.patch("promptops.request_log.cli._start", return_value=0):
                self.assertEqual(
                    main(
                        ["install", "--config-dir", str(store.root), "codex"],
                        stdout=io.StringIO(),
                        stderr=io.StringIO(),
                        environment=environment,
                    ),
                    0,
                )
            applied = target.read_bytes()
            install = ManagedConfigInstall(
                store.root / "installs", "codex", target
            )

            with mock.patch("promptops.request_log.cli._start", return_value=1):
                result = main(
                    ["install", "--config-dir", str(store.root), "codex"],
                    stdout=io.StringIO(),
                    stderr=io.StringIO(),
                    environment=environment,
                )

            self.assertEqual(result, 1)
            self.assertEqual(target.read_bytes(), applied)
            self.assertTrue(install.root.exists())
            self.assertEqual(store.load().activation_mode, "persistent")

    def test_manifest_commit_failure_stops_and_rolls_back_a_new_gateway(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            codex_home = root / "codex"
            codex_home.mkdir()
            target = codex_home / "config.toml"
            original = b'model = "gpt-test"\n'
            target.write_bytes(original)
            store = ConfigStore(root / "config")
            store.save(
                RequestLogConfig(
                    enabled=True,
                    adapters={"codex": ["openai"]},
                    save_dir=root / "logs",
                    activation_mode="session",
                )
            )

            with (
                mock.patch("promptops.request_log.cli._start", return_value=0),
                mock.patch(
                    "promptops.request_log.adapters.ManagedConfigInstall.commit",
                    side_effect=OSError("could not commit install state"),
                ),
                mock.patch("promptops.request_log.cli._stop", return_value=0) as stop,
            ):
                result = main(
                    ["install", "--config-dir", str(store.root), "codex"],
                    stdout=io.StringIO(),
                    stderr=io.StringIO(),
                    environment={**os.environ, "CODEX_HOME": str(codex_home)},
                )

            self.assertEqual(result, 2)
            stop.assert_called_once()
            self.assertEqual(target.read_bytes(), original)
            self.assertFalse((store.root / "installs" / "codex").exists())
            self.assertEqual(store.load().activation_mode, "session")

    def test_gateway_preflight_interrupt_rolls_back_a_new_install(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            codex_home = root / "codex"
            codex_home.mkdir()
            target = codex_home / "config.toml"
            original = b'model = "gpt-test"\n'
            target.write_bytes(original)
            store = ConfigStore(root / "config")
            store.save(
                RequestLogConfig(
                    enabled=True,
                    adapters={"codex": ["openai"]},
                    save_dir=root / "logs",
                    activation_mode="session",
                )
            )

            with (
                mock.patch(
                    "promptops.request_log.cli._gateway_healthy",
                    side_effect=KeyboardInterrupt,
                ),
                self.assertRaises(KeyboardInterrupt),
            ):
                main(
                    ["install", "--config-dir", str(store.root), "codex"],
                    stdout=io.StringIO(),
                    stderr=io.StringIO(),
                    environment={**os.environ, "CODEX_HOME": str(codex_home)},
                )

            self.assertEqual(target.read_bytes(), original)
            self.assertFalse((store.root / "installs" / "codex").exists())
            self.assertEqual(store.load().activation_mode, "session")

    def test_persistent_install_honors_official_agent_config_locations(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            targets = {
                "codex": root / "codex-home" / "config.toml",
                "claude-code": root / "claude-home" / "settings.json",
                "opencode": root / "custom-opencode.jsonc",
            }
            originals = {
                "codex": b'model = "gpt-test"\n',
                "claude-code": b'{"permissions":{"allow":["Read"]}}\n',
                "opencode": b'{// custom path\n"theme":"dark",}\n',
            }
            for adapter, target in targets.items():
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_bytes(originals[adapter])
            environment = {
                **os.environ,
                "CODEX_HOME": str(targets["codex"].parent),
                "CLAUDE_CONFIG_DIR": str(targets["claude-code"].parent),
                "OPENCODE_CONFIG": str(targets["opencode"]),
            }
            store = ConfigStore(root / "config")
            store.save(
                RequestLogConfig(
                    enabled=True,
                    adapters={
                        "codex": ["openai"],
                        "claude-code": ["anthropic"],
                        "opencode": ["openai"],
                    },
                    save_dir=root / "logs",
                )
            )

            with mock.patch("promptops.request_log.cli._start", return_value=0):
                for adapter in targets:
                    self.assertEqual(
                        main(
                            ["install", "--config-dir", str(store.root), adapter],
                            stdout=io.StringIO(),
                            stderr=io.StringIO(),
                            environment=environment,
                        ),
                        0,
                    )

            for adapter, target in targets.items():
                self.assertNotEqual(target.read_bytes(), originals[adapter])
                manifest = json.loads(
                    (store.root / "installs" / adapter / "install.json").read_text()
                )
                self.assertEqual(manifest["target"], str(target.resolve()))
                self.assertTrue(manifest["committed"])

    def test_disable_restores_the_recorded_target_when_agent_home_changes(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            installed_home = root / "installed-codex-home"
            installed_home.mkdir()
            installed_target = installed_home / "config.toml"
            original = b'model = "gpt-test"\n'
            installed_target.write_bytes(original)
            other_home = root / "different-codex-home"
            other_home.mkdir()
            other_target = other_home / "config.toml"
            other_original = b'model = "other"\n'
            other_target.write_bytes(other_original)
            store = ConfigStore(root / "config")
            store.save(
                RequestLogConfig(
                    enabled=True,
                    adapters={"codex": ["openai"]},
                    save_dir=root / "logs",
                )
            )

            with mock.patch("promptops.request_log.cli._start", return_value=0):
                self.assertEqual(
                    main(
                        ["install", "--config-dir", str(store.root), "codex"],
                        stdout=io.StringIO(),
                        stderr=io.StringIO(),
                        environment={**os.environ, "CODEX_HOME": str(installed_home)},
                    ),
                    0,
                )

            with mock.patch("promptops.request_log.cli._stop", return_value=0):
                result = main(
                    ["disable", "--config-dir", str(store.root), "codex"],
                    stdout=io.StringIO(),
                    stderr=io.StringIO(),
                    environment={**os.environ, "CODEX_HOME": str(other_home)},
                )

            self.assertEqual(result, 0)
            self.assertEqual(installed_target.read_bytes(), original)
            self.assertEqual(other_target.read_bytes(), other_original)

    def test_disable_all_restores_an_install_missing_from_request_config(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            codex_home = root / "codex-home"
            codex_home.mkdir()
            target = codex_home / "config.toml"
            original = b'model = "gpt-test"\n'
            target.write_bytes(original)
            store = ConfigStore(root / "config")
            config = RequestLogConfig(
                enabled=True,
                adapters={"codex": ["openai"]},
                save_dir=root / "logs",
            )
            store.save(config)
            environment = {**os.environ, "CODEX_HOME": str(codex_home)}
            with mock.patch("promptops.request_log.cli._start", return_value=0):
                self.assertEqual(
                    main(
                        ["install", "--config-dir", str(store.root), "codex"],
                        stdout=io.StringIO(),
                        stderr=io.StringIO(),
                        environment=environment,
                    ),
                    0,
                )
            config.adapters.clear()
            config.enabled = False
            store.save(config)

            with mock.patch("promptops.request_log.cli._stop", return_value=0):
                result = main(
                    ["disable", "--config-dir", str(store.root)],
                    stdout=io.StringIO(),
                    stderr=io.StringIO(),
                    environment=environment,
                )

            self.assertEqual(result, 0)
            self.assertEqual(target.read_bytes(), original)
            self.assertFalse((store.root / "installs" / "codex").exists())

    def test_persistent_opencode_install_uses_existing_global_jsonc(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            xdg_root = root / "xdg"
            target = xdg_root / "opencode" / "opencode.jsonc"
            target.parent.mkdir(parents=True)
            original = b'{// existing global config\n"theme":"dark",}\n'
            target.write_bytes(original)
            store = ConfigStore(root / "config")
            store.save(
                RequestLogConfig(
                    enabled=True,
                    adapters={"opencode": ["openai"]},
                    save_dir=root / "logs",
                )
            )
            environment = {**os.environ, "XDG_CONFIG_HOME": str(xdg_root)}

            with mock.patch("promptops.request_log.cli._start", return_value=0):
                result = main(
                    ["install", "--config-dir", str(store.root), "opencode"],
                    stdout=io.StringIO(),
                    stderr=io.StringIO(),
                    environment=environment,
                )

            self.assertEqual(result, 0)
            self.assertNotEqual(target.read_bytes(), original)
            self.assertFalse((target.parent / "opencode.json").exists())

    def test_disable_preflights_all_conflicts_before_restoring_any_adapter(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            codex_target = root / "codex" / "config.toml"
            claude_target = root / "claude" / "settings.json"
            codex_target.parent.mkdir()
            claude_target.parent.mkdir()
            codex_original = b'model = "gpt-test"\n'
            claude_original = b'{"theme":"dark"}\n'
            codex_target.write_bytes(codex_original)
            claude_target.write_bytes(claude_original)
            environment = {
                **os.environ,
                "APASTRA_CODEX_HOME": str(codex_target.parent),
                "APASTRA_CLAUDE_HOME": str(claude_target.parent),
            }
            store = ConfigStore(root / "config")
            store.save(
                RequestLogConfig(
                    enabled=True,
                    adapters={"codex": ["openai"], "claude-code": ["anthropic"]},
                    save_dir=root / "logs",
                )
            )
            with mock.patch("promptops.request_log.cli._start", return_value=0):
                for adapter in ("codex", "claude-code"):
                    self.assertEqual(
                        main(
                            ["install", "--config-dir", str(store.root), adapter],
                            stdout=io.StringIO(),
                            stderr=io.StringIO(),
                            environment=environment,
                        ),
                        0,
                    )
            claude_applied = claude_target.read_bytes()
            codex_target.write_bytes(b'model = "user-edited"\n')

            stderr = io.StringIO()
            result = main(
                ["disable", "--config-dir", str(store.root)],
                stdout=io.StringIO(),
                stderr=stderr,
                environment=environment,
            )

            self.assertEqual(result, 2)
            self.assertIn("changed after", stderr.getvalue())
            self.assertEqual(codex_target.read_bytes(), b'model = "user-edited"\n')
            self.assertEqual(claude_target.read_bytes(), claude_applied)
            self.assertTrue(store.load().enabled)

    def test_install_rejects_provider_not_enabled_for_adapter_without_writing(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            target = root / "opencode.json"
            target.write_bytes(b'{"theme":"dark"}\n')
            store = ConfigStore(root / "config")
            store.save(
                RequestLogConfig(
                    enabled=True,
                    adapters={"opencode": ["openai"]},
                    save_dir=root / "logs",
                )
            )
            stderr = io.StringIO()

            result = main(
                [
                    "install",
                    "--config-dir",
                    str(store.root),
                    "opencode",
                    "--provider",
                    "anthropic",
                ],
                stdout=io.StringIO(),
                stderr=stderr,
                environment={**os.environ, "APASTRA_OPENCODE_CONFIG": str(target)},
            )

            self.assertEqual(result, 2)
            self.assertIn("not enabled", stderr.getvalue())
            self.assertEqual(target.read_bytes(), b'{"theme":"dark"}\n')

    def test_in_repo_save_location_uses_git_info_exclude_only(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir) / "repo"
            root.mkdir()
            subprocess.run(["git", "init", "-q", str(root)], check=True)
            tracked_ignore = root / ".gitignore"
            tracked_ignore.write_text("existing-entry\n")
            config_dir = Path(temp_dir) / "config"
            save_dir = root / "private" / "request-logs"

            result = main(
                [
                    "configure",
                    "--config-dir",
                    str(config_dir),
                    "--yes",
                    "--adapters",
                    "codex:openai",
                    "--save-dir",
                    str(save_dir),
                ],
                stdout=io.StringIO(),
                stderr=io.StringIO(),
            )

            self.assertEqual(result, 0)
            self.assertEqual(tracked_ignore.read_text(), "existing-entry\n")
            exclude = root / ".git" / "info" / "exclude"
            self.assertIn("/private/request-logs/", exclude.read_text())

    def test_git_worktree_root_is_rejected_as_a_save_location(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir) / "repo"
            root.mkdir()
            subprocess.run(["git", "init", "-q", str(root)], check=True)
            config_dir = Path(temp_dir) / "config"
            stderr = io.StringIO()

            result = main(
                [
                    "configure",
                    "--config-dir",
                    str(config_dir),
                    "--yes",
                    "--adapters",
                    "codex:openai",
                    "--save-dir",
                    str(root),
                ],
                stdout=io.StringIO(),
                stderr=stderr,
            )

            self.assertEqual(result, 2)
            self.assertIn("dedicated subdirectory", stderr.getvalue())
            self.assertFalse((config_dir / "request-log.json").exists())

    def test_git_exclude_escapes_pattern_characters_in_save_path(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir) / "repo"
            root.mkdir()
            subprocess.run(["git", "init", "-q", str(root)], check=True)
            save_dir = root / "private[logs]" / "requests"

            result = main(
                [
                    "configure",
                    "--config-dir",
                    str(Path(temp_dir) / "config"),
                    "--yes",
                    "--adapters",
                    "codex:openai",
                    "--save-dir",
                    str(save_dir),
                ],
                stdout=io.StringIO(),
                stderr=io.StringIO(),
            )
            probe = save_dir / "probe.txt"
            probe.write_text("private")
            ignored = subprocess.run(
                ["git", "-C", str(root), "check-ignore", str(probe.relative_to(root))],
                text=True,
                capture_output=True,
                check=False,
            )

            self.assertEqual(result, 0)
            self.assertEqual(ignored.returncode, 0)


if __name__ == "__main__":
    unittest.main()
