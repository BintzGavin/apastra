import json
import stat
import tempfile
import unittest
from pathlib import Path

from promptops.request_log.config import (
    DEFAULT_MAX_BYTES,
    DEFAULT_RETENTION_DAYS,
    ConfigStore,
    RequestLogConfig,
)


class RequestLogConfigTests(unittest.TestCase):
    def test_fresh_config_is_disabled_and_bounded(self):
        config = RequestLogConfig.default()

        self.assertFalse(config.enabled)
        self.assertEqual(config.adapters, {})
        self.assertEqual(config.retention_days, DEFAULT_RETENTION_DAYS)
        self.assertEqual(config.max_bytes, DEFAULT_MAX_BYTES)
        self.assertEqual(config.bind_host, "127.0.0.1")

    def test_config_round_trip_preserves_selected_adapters_and_private_permissions(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            store = ConfigStore(root / "config")
            save_dir = root / "chosen logs"
            config = RequestLogConfig(
                enabled=True,
                adapters={
                    "codex": ["openai"],
                    "claude-code": ["anthropic"],
                    "opencode": ["openai", "anthropic"],
                    "pi": ["openai", "anthropic"],
                    "generic": ["openai", "anthropic"],
                },
                save_dir=save_dir,
                activation_mode="session",
                retention_days=7,
                max_bytes=250 * 1024 * 1024,
            )

            store.save(config)
            loaded = store.load()

            self.assertEqual(loaded, config.normalized())
            self.assertEqual(stat.S_IMODE(store.path.stat().st_mode), 0o600)
            self.assertEqual(stat.S_IMODE(store.root.stat().st_mode), 0o700)

    def test_rejects_non_loopback_bind_address(self):
        config = RequestLogConfig.default()
        config.bind_host = "0.0.0.0"

        with self.assertRaisesRegex(ValueError, "loopback"):
            config.validate()

    def test_rejects_unknown_adapter_or_provider(self):
        for adapters in ({"cursor": ["openai"]}, {"codex": ["gemini"]}):
            with self.subTest(adapters=adapters):
                config = RequestLogConfig.default()
                config.adapters = adapters
                with self.assertRaises(ValueError):
                    config.validate()

    def test_enabled_config_requires_an_adapter(self):
        config = RequestLogConfig.default()
        config.enabled = True

        with self.assertRaisesRegex(ValueError, "adapter"):
            config.validate()

    def test_upstreams_must_be_credential_free_origins(self):
        invalid_origins = (
            "https://secret@api.openai.com",
            "https://api.openai.com?key=secret",
            "https://api.openai.com#fragment",
            "https://api.openai.com:invalid",
        )
        for origin in invalid_origins:
            with self.subTest(origin=origin):
                config = RequestLogConfig.default()
                config.upstreams["openai"] = origin
                with self.assertRaisesRegex(ValueError, "origin"):
                    config.validate()

    def test_unknown_config_fields_report_a_validation_error(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            store = ConfigStore(Path(temp_dir))
            store.path.write_text(json.dumps({"future_field": True}))

            with self.assertRaisesRegex(ValueError, "Unknown request-log configuration field"):
                store.load()

    def test_malformed_save_directory_reports_a_validation_error(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            store = ConfigStore(Path(temp_dir))
            store.path.write_text(json.dumps({"save_dir": ["not", "a", "path"]}))

            with self.assertRaisesRegex(ValueError, "Invalid request-log configuration"):
                store.load()

    def test_malformed_typed_values_report_a_validation_error(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            store = ConfigStore(Path(temp_dir))
            store.path.write_text(json.dumps({"bind_port": "not-a-port"}))

            with self.assertRaisesRegex(ValueError, "Invalid request-log configuration"):
                store.load()

    def test_indefinite_retention_requires_explicit_acknowledgement(self):
        config = RequestLogConfig.default()
        config.retention_days = 0
        config.max_bytes = 0

        with self.assertRaisesRegex(ValueError, "indefinite"):
            config.validate()

        config.indefinite_retention_confirmed = True
        config.validate()


if __name__ == "__main__":
    unittest.main()
