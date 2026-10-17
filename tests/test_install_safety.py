"""Installation must preserve the source and unrelated consumer files."""
import json
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest

from tests.test_installed_contract import ROOT, isolated_environment


class InstallSafetyTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory(prefix="apastra-install-safety-")
        self.addCleanup(self.temporary.cleanup)
        self.directory = Path(self.temporary.name)
        self.project = self.directory / "consumer"
        self.project.mkdir()
        self.source = self.project / ".agent/skills/apastra"
        shutil.copytree(ROOT, self.source, ignore=shutil.ignore_patterns(
            ".git", ".venv", "node_modules", "*.tgz", "__pycache__", "*.pyc"))
        (self.source / ".git").mkdir()
        (self.source / ".git/HEAD").write_text("ref: refs/heads/main\n")
        (self.source / "source-sentinel.txt").write_text("keep source")
        evidence = self.source / "promptops/runs/synthetic-evidence"
        evidence.mkdir()
        (evidence / "run_manifest.json").write_text('{"private": "synthetic"}')
        results = self.source / "promptops/harnesses/experimental-results"
        results.mkdir()
        (results / "metrics.json").write_text('{"score": 0.5}')
        (results / "metrics.yaml").write_text("score: 0.5\n")
        (self.source / "promptops/harnesses/promptfoo/experimental-results.yaml").write_text("score: 0.5\n")
        self.environment = {**isolated_environment(self.directory), "APASTRA_ASSUME_YES": "1",
                            "APASTRA_NO_AGENT_HOOKS": "1"}

    def setup(self, *arguments):
        return subprocess.run([str(self.source / "setup"), *arguments], cwd=self.project,
                              env=self.environment, text=True, capture_output=True, timeout=30)

    def test_setup_preserves_clone_and_unknown_files_and_is_repeatable(self):
        for attempt in range(2):
            result = self.setup()
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertEqual((self.source / "source-sentinel.txt").read_text(), "keep source")
            self.assertEqual((self.source / ".git/HEAD").read_text(), "ref: refs/heads/main\n")
            self.assertTrue((self.source / "promptops/runtime/cli.py").is_file())
            runtime = self.project / ".agent/scripts/apastra"
            if attempt == 0:
                (runtime / "user-notes.txt").write_text("keep consumer")
            self.assertEqual((runtime / "user-notes.txt").read_text(), "keep consumer")
            self.assertFalse(any((runtime / "runs").glob("*/run_manifest.json")))
            self.assertTrue((runtime / "runs/runner-shim.sh").is_file())
            self.assertFalse((runtime / "harnesses/experimental-results").exists())
            self.assertFalse((runtime / "harnesses/promptfoo/experimental-results.yaml").exists())
            for name in ("run.py", "adapter.yaml", "README.md"):
                bridge = Path("harnesses/promptfoo") / name
                self.assertEqual((runtime / bridge).read_bytes(), (self.source / "promptops" / bridge).read_bytes())
            self.assertEqual((self.project / ".agents/skills/apastra").resolve(), self.source.resolve())
        unrelated = self.directory / "unrelated"
        unrelated.mkdir()
        result = subprocess.run([str(self.project / ".agent/bin/apastra"), "request-log", "status",
                                 "--config-dir", str(unrelated / "config"), "--json"], cwd=unrelated,
                                env=self.environment, text=True, capture_output=True, timeout=15)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertFalse(json.loads(result.stdout)["enabled"])

    def test_tracked_upgrade_succeeds_and_user_edit_is_preserved(self):
        self.assertEqual(self.setup().returncode, 0)
        source_file = self.source / "promptops/runtime/entrypoint.py"
        destination = self.project / ".agent/scripts/apastra/runtime/entrypoint.py"
        source_file.write_text(source_file.read_text() + "\n# upgrade\n")
        result = self.setup()
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertEqual(destination.read_text(), source_file.read_text())
        destination.write_text("# consumer customization\n")
        source_file.write_text(source_file.read_text() + "# second upgrade\n")
        result = self.setup()
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("Preserving conflicting user file", result.stderr)
        self.assertEqual(destination.read_text(), "# consumer customization\n")
        self.assertFalse((self.project / ".agent/.apastra-install.lock").exists())

    def test_retry_accepts_partial_upgrade_with_previous_manifest(self):
        self.assertEqual(self.setup().returncode, 0)
        source_file = self.source / "promptops/runtime/entrypoint.py"
        source_file.write_text(source_file.read_text() + "\n# interrupted upgrade\n")
        destination = self.project / ".agent/scripts/apastra/runtime/entrypoint.py"
        # Model interruption after an atomic file replacement but before the new
        # manifest was written. The retry must accept the already-copied payload.
        shutil.copyfile(source_file, destination)
        result = self.setup()
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertEqual(destination.read_text(), source_file.read_text())
        self.assertTrue((self.source / ".git/HEAD").is_file())

    def test_unknown_install_manifest_is_preserved(self):
        manifest = self.project / ".agent/.apastra-install.json"
        manifest.write_text('{"user": "notes"}')
        result = self.setup()
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(manifest.read_text(), '{"user": "notes"}')
        self.assertFalse((self.project / ".agent/scripts").exists())

    def test_existing_install_lock_blocks_concurrent_install(self):
        lock = self.project / ".agent/.apastra-install.lock"
        lock.mkdir()
        result = self.setup()
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("Another install is active", result.stderr)
        self.assertTrue(lock.is_dir())
        self.assertFalse((self.project / ".agent/scripts").exists())

    def test_dry_run_does_not_write_or_prune(self):
        result = self.setup("--dry-run")
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertTrue((self.source / "source-sentinel.txt").is_file())
        self.assertFalse((self.project / ".agent/bin").exists())

    def test_symlink_destination_fails_without_writing_outside_project(self):
        outside = self.directory / "outside"
        outside.mkdir()
        (self.project / ".agent/scripts").symlink_to(outside, target_is_directory=True)
        result = self.setup()
        self.assertNotEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertEqual(list(outside.iterdir()), [])
        self.assertFalse((self.project / ".agent/bin").exists())
        self.assertTrue((self.source / "source-sentinel.txt").is_file())

    def test_conflicting_unknown_file_fails_before_copy(self):
        cli = self.project / ".agent/bin/apastra"
        cli.parent.mkdir(parents=True)
        cli.write_text("user executable")
        result = self.setup()
        self.assertNotEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertEqual(cli.read_text(), "user executable")
        self.assertFalse((self.project / ".agent/scripts").exists())


if __name__ == "__main__":
    unittest.main()
