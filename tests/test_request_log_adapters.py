import json
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from promptops.request_log import adapters as request_log_adapters
from promptops.request_log.adapters import (
    ManagedConfigInstall,
    build_session_launch,
    persistent_config_bytes,
)


class SessionAdapterTests(unittest.TestCase):
    def setUp(self):
        self.gateway = "http://127.0.0.1:43123"

    def test_codex_uses_process_argument_override(self):
        launch = build_session_launch(
            "codex", ["--model", "gpt-test"], self.gateway, providers=["openai"]
        )

        self.assertEqual(launch.command[0], "codex")
        self.assertIn(
            'openai_base_url="http://127.0.0.1:43123/openai/codex/v1"', launch.command
        )
        self.assertEqual(launch.command[-2:], ["--model", "gpt-test"])
        self.assertEqual(launch.environment, {})

    def test_claude_code_uses_child_environment_only(self):
        launch = build_session_launch(
            "claude-code",
            ["--model", "claude-test"],
            self.gateway,
            providers=["anthropic"],
        )

        self.assertEqual(launch.command, ["claude", "--model", "claude-test"])
        self.assertEqual(
            launch.environment["ANTHROPIC_BASE_URL"],
            f"{self.gateway}/anthropic/claude-code",
        )

    def test_opencode_merges_inline_config_for_both_providers(self):
        existing = json.dumps(
            {"theme": "dark", "provider": {"openai": {"options": {"timeout": 50}}}}
        )
        launch = build_session_launch(
            "opencode",
            [],
            self.gateway,
            providers=["openai", "anthropic"],
            parent_environment={"OPENCODE_CONFIG_CONTENT": existing},
        )

        config = json.loads(launch.environment["OPENCODE_CONFIG_CONTENT"])
        self.assertEqual(config["theme"], "dark")
        self.assertEqual(config["provider"]["openai"]["options"]["timeout"], 50)
        self.assertEqual(
            config["provider"]["openai"]["options"]["baseURL"],
            f"{self.gateway}/openai/opencode/v1",
        )
        self.assertEqual(
            config["provider"]["anthropic"]["options"]["baseURL"],
            f"{self.gateway}/anthropic/opencode/v1",
        )

    def test_opencode_rejects_a_non_object_provider_config(self):
        with self.assertRaisesRegex(ValueError, "provider"):
            build_session_launch(
                "opencode",
                [],
                self.gateway,
                providers=["openai"],
                parent_environment={"OPENCODE_CONFIG_CONTENT": '{"provider":[]}'},
            )

    def test_pi_uses_isolated_agent_dir_and_preserves_existing_resources(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            source = Path(temp_dir) / "pi-home"
            source.mkdir()
            (source / "auth.json").write_text(
                '{"anthropic":{"token":"not copied into models"}}'
            )
            (source / "models.json").write_text(
                '{"providers":{"anthropic":{"headers":{"x-test":"yes"}}}}'
            )

            launch = build_session_launch(
                "pi",
                [],
                self.gateway,
                providers=["openai", "anthropic"],
                pi_agent_dir=source,
                temp_root=Path(temp_dir) / "sessions",
            )
            isolated = Path(launch.environment["PI_CODING_AGENT_DIR"])
            models = json.loads((isolated / "models.json").read_text())

            self.assertNotEqual(isolated, source)
            self.assertTrue((isolated / "auth.json").is_symlink())
            self.assertEqual(
                models["providers"]["anthropic"]["headers"], {"x-test": "yes"}
            )
            self.assertEqual(
                models["providers"]["anthropic"]["baseUrl"],
                f"{self.gateway}/anthropic/pi/v1",
            )
            self.assertEqual(
                models["providers"]["openai"]["baseUrl"], f"{self.gateway}/openai/pi/v1"
            )
            launch.cleanup()
            self.assertFalse(isolated.exists())

    def test_pi_session_accepts_documented_jsonc_models_config(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            source = Path(temp_dir) / "pi-home"
            source.mkdir()
            (source / "models.json").write_text(
                """{
                  // Pi models.json supports comments and trailing commas.
                  "providers": {
                    "anthropic": {"headers": {"x-test": "yes",},},
                  },
                }\n"""
            )

            launch = build_session_launch(
                "pi",
                [],
                self.gateway,
                providers=["anthropic"],
                pi_agent_dir=source,
                temp_root=Path(temp_dir) / "sessions",
            )
            try:
                isolated = Path(launch.environment["PI_CODING_AGENT_DIR"])
                models = json.loads((isolated / "models.json").read_text())
                self.assertEqual(
                    models["providers"]["anthropic"]["headers"], {"x-test": "yes"}
                )
                self.assertEqual(
                    models["providers"]["anthropic"]["baseUrl"],
                    f"{self.gateway}/anthropic/pi/v1",
                )
            finally:
                launch.cleanup()

    def test_generic_client_receives_both_provider_base_urls(self):
        launch = build_session_launch(
            "generic", ["my-agent"], self.gateway, providers=["openai", "anthropic"]
        )

        self.assertEqual(launch.command, ["my-agent"])
        self.assertEqual(
            launch.environment["OPENAI_BASE_URL"], f"{self.gateway}/openai/generic/v1"
        )
        self.assertEqual(
            launch.environment["ANTHROPIC_BASE_URL"],
            f"{self.gateway}/anthropic/generic",
        )


class PersistentAdapterTests(unittest.TestCase):
    def test_partial_target_write_is_rolled_back_for_existing_and_new_configs(self):
        for target_existed in (True, False):
            with (
                self.subTest(target_existed=target_existed),
                tempfile.TemporaryDirectory() as temp_dir,
            ):
                root = Path(temp_dir)
                target = root / "settings.json"
                original = b'{"theme":"old"}\n'
                if target_existed:
                    target.write_bytes(original)
                install = ManagedConfigInstall(root / "state", "opencode", target)
                applied = b'{"provider":{"openai":{}}}\n'
                real_write = request_log_adapters._write_atomic_private
                calls = 0

                def fail_first_write(path, data):
                    nonlocal calls
                    calls += 1
                    if calls == 1:
                        path.parent.mkdir(parents=True, exist_ok=True)
                        path.write_bytes(data)
                        raise OSError("simulated interrupted config write")
                    return real_write(path, data)

                with (
                    mock.patch(
                        "promptops.request_log.adapters._write_atomic_private",
                        side_effect=fail_first_write,
                    ),
                    self.assertRaisesRegex(OSError, "interrupted"),
                ):
                    install.apply(applied)

                if target_existed:
                    self.assertEqual(target.read_bytes(), original)
                else:
                    self.assertFalse(target.exists())
                self.assertFalse(install.root.exists())

    def test_nested_adapter_configuration_must_be_an_object(self):
        fixtures = (
            ("claude-code", b'{"env":[]}\n', ["anthropic"]),
            ("opencode", b'{"provider":[]}\n', ["openai"]),
            ("pi", b'{"providers":[]}\n', ["anthropic"]),
        )
        for adapter, original, providers in fixtures:
            with (
                self.subTest(adapter=adapter),
                self.assertRaisesRegex(ValueError, "object"),
            ):
                persistent_config_bytes(
                    adapter, original, "http://127.0.0.1:43123", providers
                )

    def test_each_adapter_preserves_unrelated_config(self):
        gateway = "http://127.0.0.1:43123"
        fixtures = {
            "codex": b'model = "gpt-test"\nmodel_reasoning_effort = "high"\n',
            "claude-code": b'{"permissions":{"allow":["Read"]}}\n',
            "opencode": b'{"theme":"dark"}\n',
            "pi": b'{"providers":{"anthropic":{"headers":{"x-test":"yes"}}}}\n',
            "generic": b'{"environment":{"OTHER_SETTING":"preserved"},"theme":"dark"}\n',
        }

        for adapter, original in fixtures.items():
            with self.subTest(adapter=adapter):
                applied = persistent_config_bytes(
                    adapter, original, gateway, ["openai", "anthropic"]
                )
                text = applied.decode()
                self.assertIn("43123", text)
                if adapter == "codex":
                    self.assertIn('model = "gpt-test"', text)
                else:
                    parsed = json.loads(text)
                    self.assertIsInstance(parsed, dict)
                    if adapter == "generic":
                        self.assertEqual(
                            parsed["environment"]["OTHER_SETTING"], "preserved"
                        )

    def test_opencode_persistent_config_accepts_jsonc(self):
        original = b"""{
          // OpenCode documents JSON with comments.
          "theme": "dark",
          "homepage": "https://example.com/a//b",
          "provider": {
            "openai": {"options": {"timeout": 50,},},
          },
        }\n"""

        applied = persistent_config_bytes(
            "opencode",
            original,
            "http://127.0.0.1:43123",
            ["openai", "anthropic"],
        )
        parsed = json.loads(applied)

        self.assertEqual(parsed["theme"], "dark")
        self.assertEqual(parsed["homepage"], "https://example.com/a//b")
        self.assertEqual(parsed["provider"]["openai"]["options"]["timeout"], 50)
        self.assertIn(
            "/openai/opencode/v1", parsed["provider"]["openai"]["options"]["baseURL"]
        )
        self.assertIn(
            "/anthropic/opencode/v1",
            parsed["provider"]["anthropic"]["options"]["baseURL"],
        )

    def test_pi_persistent_config_accepts_documented_jsonc(self):
        original = b"""{
          // Pi models.json supports JSONC.
          "providers": {
            "openai": {"headers": {"x-test": "yes",},},
          },
        }\n"""

        applied = persistent_config_bytes(
            "pi",
            original,
            "http://127.0.0.1:43123",
            ["openai"],
        )
        parsed = json.loads(applied)

        self.assertEqual(parsed["providers"]["openai"]["headers"], {"x-test": "yes"})
        self.assertIn("/openai/pi/v1", parsed["providers"]["openai"]["baseUrl"])

    def test_pi_jsonc_preserves_string_content_that_resembles_trailing_commas(self):
        original = b'''{
          "label": "literal,}",
          "providers": {
            "anthropic": {"note": "literal,]",},
          },
        }\n'''

        applied = persistent_config_bytes(
            "pi",
            original,
            "http://127.0.0.1:43123",
            ["anthropic"],
        )
        parsed = json.loads(applied)

        self.assertEqual(parsed["label"], "literal,}")
        self.assertEqual(parsed["providers"]["anthropic"]["note"], "literal,]")
        self.assertIn(
            "/anthropic/pi/v1", parsed["providers"]["anthropic"]["baseUrl"]
        )

    def test_pi_rejects_an_unterminated_jsonc_block_comment(self):
        with self.assertRaisesRegex(ValueError, "Unterminated JSONC block comment"):
            persistent_config_bytes(
                "pi",
                b'{"providers":{"anthropic":{}}} /* unterminated',
                "http://127.0.0.1:43123",
                ["anthropic"],
            )

    def test_pi_rejects_jsonc_comments_that_would_merge_invalid_tokens(self):
        with self.assertRaisesRegex(ValueError, "not valid JSON"):
            persistent_config_bytes(
                "pi",
                b'{"limit":1/* missing comma */2,"providers":{"anthropic":{}}}',
                "http://127.0.0.1:43123",
                ["anthropic"],
            )

    def test_install_restore_and_conflict_detection(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            target = root / "settings.json"
            target.write_bytes(b'{"theme":"old"}\n')
            install = ManagedConfigInstall(root / "state", "opencode", target)

            install.apply(b'{"theme":"old","provider":{"openai":{}}}\n')
            self.assertNotEqual(target.read_bytes(), b'{"theme":"old"}\n')
            install.restore()
            self.assertEqual(target.read_bytes(), b'{"theme":"old"}\n')

            install.apply(b'{"theme":"old","provider":{"openai":{}}}\n')
            target.write_bytes(b'{"theme":"user-edited"}\n')
            with self.assertRaisesRegex(RuntimeError, "changed after"):
                install.restore()
            self.assertEqual(target.read_bytes(), b'{"theme":"user-edited"}\n')
            self.assertTrue(install.backup_path.exists())

    def test_restore_rejects_a_corrupted_backup_before_changing_target(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            target = root / "settings.json"
            target.write_bytes(b'{"theme":"old"}\n')
            install = ManagedConfigInstall(root / "state", "opencode", target)
            applied = b'{"theme":"old","provider":{"openai":{}}}\n'
            install.apply(applied)
            install.backup_path.write_bytes(b"corrupted")

            with self.assertRaisesRegex(RuntimeError, "backup"):
                install.restore()

            self.assertEqual(target.read_bytes(), applied)

    def test_reinstall_rejects_different_applied_bytes(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            target = root / "settings.json"
            target.write_bytes(b'{"theme":"old"}\n')
            install = ManagedConfigInstall(root / "state", "opencode", target)
            first = b'{"provider":{"openai":{}}}\n'
            second = b'{"provider":{"anthropic":{}}}\n'
            install.apply(first)

            with self.assertRaisesRegex(RuntimeError, "disable.*changing"):
                install.apply(second)

            self.assertEqual(target.read_bytes(), first)
            self.assertTrue(install.backup_path.exists())

    def test_prepared_install_state_can_be_retried_or_disabled(self):
        for action in ("retry", "disable"):
            with self.subTest(action=action), tempfile.TemporaryDirectory() as temp_dir:
                root = Path(temp_dir)
                target = root / "settings.json"
                original = b'{"theme":"old"}\n'
                applied = b'{"theme":"old","provider":{"openai":{}}}\n'
                target.write_bytes(original)
                install = ManagedConfigInstall(root / "state", "opencode", target)
                install.root.mkdir(parents=True)
                install.backup_path.write_bytes(original)
                install.manifest_path.write_text(
                    json.dumps(
                        {
                            "schema_version": 1,
                            "adapter": "opencode",
                            "target": str(target.resolve()),
                            "target_existed": True,
                            "original_digest": request_log_adapters._digest(original),
                            "applied_digest": request_log_adapters._digest(applied),
                        }
                    )
                )

                if action == "retry":
                    install.apply(applied)
                    self.assertEqual(target.read_bytes(), applied)
                    self.assertTrue(install.manifest_path.exists())
                else:
                    install.restore()
                    self.assertEqual(target.read_bytes(), original)
                    self.assertFalse(install.root.exists())


if __name__ == "__main__":
    unittest.main()
