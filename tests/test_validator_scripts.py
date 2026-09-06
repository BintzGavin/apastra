import json
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


@unittest.skipUnless(shutil.which("node"), "node is required for validator scripts")
class ValidatorScriptTests(unittest.TestCase):
    def test_duplicate_json_keys_and_nonfinite_yaml_are_rejected(self):
        samples = [('request.json', '{"id":"one","id":"two","template":"text","variables":{}}'),
                   ('request.yaml', 'id: one\ntemplate: text\nvariables: {}\nextra: .nan\n')]
        with tempfile.TemporaryDirectory() as directory:
            for filename, content in samples:
                path = Path(directory) / filename
                path.write_text(content)
                result = subprocess.run(["bash", str(ROOT / "promptops/validators/validate-prompt-spec.sh"), str(path)], cwd=directory, capture_output=True, text=True)
                self.assertNotEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_validator_resolves_its_schema_outside_the_workspace(self):
        with tempfile.TemporaryDirectory() as directory:
            result = subprocess.run(
                ["bash", str(ROOT / "promptops/validators/validate-regression-policy.sh"), str(ROOT / "promptops/policies/regression.yaml")],
                cwd=directory, capture_output=True, text=True,
            )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_reject_validator_fails_when_no_input_is_supplied(self):
        result = subprocess.run(
            ["bash", str(ROOT / "promptops/validators/validate-reject-record.sh")],
            cwd=ROOT, capture_output=True, text=True,
        )
        self.assertNotEqual(result.returncode, 0)

    def test_quick_eval_validates_referenced_cases(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "eval.yaml"
            for case, expected in [("case_id: one\n    inputs: {text: hello}", 0), ("inputs: {text: hello}", 1)]:
                with self.subTest(case=case):
                    path.write_text("id: demo\nprompt: 'Summarize {{text}}'\ncases:\n  - " + case + "\n")
                    result = subprocess.run(
                        ["bash", str(ROOT / "promptops/validators/validate-quick-eval.sh"), str(path)],
                        cwd=ROOT, capture_output=True, text=True,
                    )
                    self.assertEqual(result.returncode, expected, result.stdout + result.stderr)

    def run_validator(self, script, fixture):
        result = subprocess.run(
            ["bash", str(ROOT / script), str(ROOT / fixture)],
            cwd=ROOT,
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(
            result.returncode,
            0,
            msg=result.stdout + result.stderr,
        )

    def test_regression_policy_validator_accepts_yaml_without_yq(self):
        self.run_validator(
            "promptops/validators/validate-regression-policy.sh",
            "promptops/policies/regression.yaml",
        )

    def test_delivery_target_validator_accepts_shipped_target_fixtures(self):
        fixtures = [
            "promptops/delivery/mcp-server-target.yaml",
            "promptops/delivery/npm-target.yaml",
            "promptops/delivery/oci-target.yaml",
            "promptops/delivery/prod-target.yaml",
            "promptops/delivery/pypi-target.yaml",
            "promptops/delivery/release-descriptor-target.yaml",
        ]

        for fixture in fixtures:
            with self.subTest(fixture=fixture):
                self.run_validator(
                    "promptops/validators/validate-delivery-target.sh",
                    fixture,
                )


class OfflineValidatorDependencyTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        self.installation = self.root / "installation with spaces"
        self.consumer = self.root / "unrelated consumer"
        self.consumer.mkdir()
        self.bin_dir = self.root / "bin"
        self.bin_dir.mkdir()
        for name in ("validators", "schemas"):
            shutil.copytree(ROOT / "promptops" / name, self.installation / "promptops" / name)
        node = subprocess.check_output(["node", "-p", "process.execPath"], text=True).strip()
        (self.bin_dir / "node").symlink_to(node)
        for command in ("npm", "npx"):
            stub = self.bin_dir / command
            stub.write_text("#!/bin/sh\necho 'Package-manager invocation forbidden by offline test' >&2\nexit 93\n")
            stub.chmod(0o755)
        # Use only known tool locations; do not inherit or inspect process secrets.
        self.child_environment = {"PATH": f"{self.bin_dir}:/usr/bin:/bin"}

    def assert_pack_validation(self):
        pack = {"id": "offline", "name": "Offline pack", "description": "Fixture", "custodian": "tests"}
        for valid in (True, False):
            with self.subTest(valid=valid):
                fixture = dict(pack)
                if not valid:
                    del fixture["custodian"]
                (self.consumer / "pack.json").write_text(json.dumps(fixture))
                result = subprocess.run(
                    ["/bin/bash", str(self.installation / "promptops/validators/validate-community-prompt-pack.sh"), "pack.json"],
                    cwd=self.consumer, env=self.child_environment, capture_output=True, text=True, timeout=15,
                )
                self.assertEqual(result.returncode, 0 if valid else 1, result.stdout + result.stderr)
                self.assertNotIn("Package-manager invocation", result.stderr)
                if not valid:
                    self.assertIn("custodian", result.stdout + result.stderr)

    def test_uses_available_ajv_from_unrelated_directory_without_npm(self):
        global_modules = self.root / "global tools/node_modules"
        shutil.copytree(ROOT / "node_modules", global_modules, symlinks=True)
        (self.bin_dir / "ajv").symlink_to(global_modules / "ajv-cli/dist/index.js")
        self.assert_pack_validation()

    def test_uses_installed_package_dependencies_without_ajv_on_path(self):
        shutil.copytree(ROOT / "node_modules", self.installation / "node_modules", symlinks=True)
        self.assert_pack_validation()

    def test_missing_dependencies_fail_explicitly_without_attempting_installation(self):
        (self.consumer / "pack.json").write_text("{}")
        result = subprocess.run(
            ["/bin/bash", str(self.installation / "promptops/validators/validate-community-prompt-pack.sh"), "pack.json"],
            cwd=self.consumer, env=self.child_environment, capture_output=True, text=True, timeout=15,
        )
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("AJV is not installed", result.stderr)
        self.assertNotIn("Package-manager invocation", result.stderr)


if __name__ == "__main__":
    unittest.main()
