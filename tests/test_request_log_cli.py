import io
import json
import tempfile
import unittest
from pathlib import Path

from promptops.request_log.artifacts import RequestArtifactStore
from promptops.request_log.cli import _parser, main
from promptops.request_log.config import ConfigStore, RequestLogConfig


class RequestLogCliTests(unittest.TestCase):
    def test_run_parses_provider_after_adapter_and_preserves_agent_arguments(self):
        args = _parser().parse_args(
            ["run", "codex", "--provider", "openai", "--", "--model", "gpt-test"]
        )

        self.assertEqual(args.adapter, "codex")
        self.assertEqual(args.provider, ["openai"])
        self.assertEqual(args.agent_args, ["--model", "gpt-test"])

    def test_configure_aliases_complete_the_same_opt_in_flow(self):
        for command in ("onboard", "enable"):
            with self.subTest(command=command), tempfile.TemporaryDirectory() as temp_dir:
                root = Path(temp_dir)
                result = main(
                    [
                        command,
                        "--config-dir",
                        str(root / "config"),
                        "--yes",
                        "--adapters",
                        "codex:openai",
                        "--save-dir",
                        str(root / "logs"),
                    ],
                    stdout=io.StringIO(),
                    stderr=io.StringIO(),
                )

                self.assertEqual(result, 0)
                self.assertTrue(ConfigStore(root / "config").load().enabled)

    def test_reconfigure_refuses_to_orphan_a_persistent_restore_point(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            store = ConfigStore(root / "config")
            original = RequestLogConfig(
                enabled=True,
                adapters={"generic": ["openai"]},
                save_dir=root / "old-logs",
            )
            store.save(original)
            install_state = store.root / "installs" / "generic" / "install.json"
            install_state.parent.mkdir(parents=True)
            install_state.write_text("{}")
            stderr = io.StringIO()

            result = main(
                [
                    "configure",
                    "--config-dir",
                    str(store.root),
                    "--yes",
                    "--adapters",
                    "codex:openai",
                    "--save-dir",
                    str(root / "new-logs"),
                ],
                stdout=io.StringIO(),
                stderr=stderr,
            )

            self.assertEqual(result, 2)
            self.assertIn("disable", stderr.getvalue().lower())
            self.assertEqual(store.load(), original.normalized())

    def test_configure_requires_explicit_yes(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            stdout = io.StringIO()

            result = main(
                ["configure", "--config-dir", str(root / "config")],
                input_fn=lambda _prompt: "",
                stdout=stdout,
                stderr=io.StringIO(),
            )

            self.assertEqual(result, 0)
            self.assertFalse(ConfigStore(root / "config").load().enabled)
            self.assertIn("remains disabled", stdout.getvalue())

    def test_noninteractive_configure_records_adapter_and_save_choices(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            stdout = io.StringIO()
            result = main(
                [
                    "configure",
                    "--config-dir",
                    str(root / "config"),
                    "--yes",
                    "--adapters",
                    "codex:openai,claude-code:anthropic,opencode:openai+anthropic,pi:openai+anthropic,generic:openai+anthropic",
                    "--save-dir",
                    str(root / "my logs"),
                    "--mode",
                    "session",
                    "--retention-days",
                    "7",
                    "--max-mb",
                    "250",
                ],
                input_fn=lambda _prompt: self.fail("noninteractive configure prompted"),
                stdout=stdout,
                stderr=io.StringIO(),
            )

            config = ConfigStore(root / "config").load()
            self.assertEqual(result, 0)
            self.assertTrue(config.enabled)
            self.assertEqual(config.save_dir, (root / "my logs").resolve())
            self.assertEqual(config.adapters["pi"], ["openai", "anthropic"])
            self.assertIn("apastra request-log run codex", stdout.getvalue())

    def test_noninteractive_indefinite_retention_requires_flag_without_prompting(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            stderr = io.StringIO()

            result = main(
                [
                    "configure",
                    "--config-dir",
                    str(root / "config"),
                    "--yes",
                    "--adapters",
                    "codex:openai",
                    "--save-dir",
                    str(root / "logs"),
                    "--retention-days",
                    "0",
                ],
                input_fn=lambda _prompt: self.fail("noninteractive configure prompted"),
                stdout=io.StringIO(),
                stderr=stderr,
            )

            self.assertEqual(result, 2)
            self.assertIn("--indefinite-retention", stderr.getvalue())

    def test_status_json_is_machine_readable(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            stdout = io.StringIO()
            result = main(
                ["status", "--config-dir", str(root / "config"), "--json"],
                stdout=stdout,
                stderr=io.StringIO(),
            )

            payload = json.loads(stdout.getvalue())
            self.assertEqual(result, 0)
            self.assertFalse(payload["enabled"])
            self.assertEqual(payload["adapters"], {})
            self.assertEqual(payload["config_dir"], str((root / "config").resolve()))

    def test_list_show_and_prune_use_configured_save_directory(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            configure_out = io.StringIO()
            main(
                [
                    "configure",
                    "--config-dir",
                    str(root / "config"),
                    "--yes",
                    "--adapters",
                    "codex:openai",
                    "--save-dir",
                    str(root / "logs"),
                    "--mode",
                    "session",
                ],
                stdout=configure_out,
                stderr=io.StringIO(),
            )
            store = RequestArtifactStore(root / "logs")
            artifact = store.begin_request("openai", "codex", "POST", "/v1/responses", "application/json", b'{"model":"gpt-test"}')
            store.complete_request(artifact.request_id, 200, 1)

            list_out = io.StringIO()
            show_out = io.StringIO()
            prune_out = io.StringIO()
            self.assertEqual(main(["list", "--config-dir", str(root / "config"), "--json"], stdout=list_out, stderr=io.StringIO()), 0)
            self.assertEqual(main(["show", artifact.request_id, "--config-dir", str(root / "config"), "--json"], stdout=show_out, stderr=io.StringIO()), 0)
            self.assertEqual(main(["prune", "--config-dir", str(root / "config"), "--json"], stdout=prune_out, stderr=io.StringIO()), 0)
            self.assertEqual(json.loads(list_out.getvalue())[0]["request_id"], artifact.request_id)
            self.assertEqual(json.loads(show_out.getvalue())["body"]["model"], "gpt-test")
            self.assertEqual(json.loads(prune_out.getvalue()), {"removed": []})


if __name__ == "__main__":
    unittest.main()
