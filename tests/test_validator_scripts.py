import shutil
import subprocess
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


@unittest.skipUnless(shutil.which("npx"), "npx is required for validator scripts")
class ValidatorScriptTests(unittest.TestCase):
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


if __name__ == "__main__":
    unittest.main()
