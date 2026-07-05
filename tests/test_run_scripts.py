import hashlib
import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
import uuid
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[1]


class RunScriptTests(unittest.TestCase):
    def test_compute_digest_handles_yaml_without_yq(self):
        source = ROOT / "promptops/policies/regression.yaml"
        with source.open("r", encoding="utf-8") as handle:
            data = yaml.safe_load(handle)
        canonical = json.dumps(data, sort_keys=True, separators=(",", ":"))
        expected = "sha256:" + hashlib.sha256(canonical.encode("utf-8")).hexdigest()

        result = subprocess.run(
            ["bash", str(ROOT / "promptops/validators/compute-digest.sh"), str(source)],
            cwd=ROOT,
            env={**os.environ, "PYTHON": sys.executable},
            capture_output=True,
            text=True,
            check=False,
        )

        self.assertEqual(result.returncode, 0, msg=result.stdout + result.stderr)
        self.assertEqual(result.stdout.strip(), expected)

    def test_runner_shim_extracts_yaml_entrypoint_without_yq(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            harness = tmp_path / "fake-harness.sh"
            adapter = tmp_path / "adapter.yaml"
            run_request = tmp_path / "run-request.json"
            output_dir = tmp_path / "out"

            harness.write_text(
                "\n".join(
                    [
                        "#!/bin/sh",
                        "set -eu",
                        "mkdir -p \"$2\"",
                        "printf '{\"ok\":true}\\n' > \"$2/run_manifest.json\"",
                        "",
                    ]
                ),
                encoding="utf-8",
            )
            harness.chmod(0o755)
            adapter.write_text(
                f"entrypoint: {harness}\n",
                encoding="utf-8",
            )
            run_request.write_text("{}", encoding="utf-8")

            result = subprocess.run(
                [
                    "bash",
                    str(ROOT / "promptops/runs/runner-shim.sh"),
                    str(adapter),
                    str(run_request),
                    str(output_dir),
                ],
                cwd=ROOT,
                env={**os.environ, "PYTHON": sys.executable},
                capture_output=True,
                text=True,
                check=False,
            )

            self.assertEqual(result.returncode, 0, msg=result.stdout + result.stderr)
            self.assertTrue((output_dir / "run_manifest.json").exists())

    def test_generate_community_baselines_reads_yaml_without_yq(self):
        suite_id = f"test-community-{uuid.uuid4().hex}"
        output_path = ROOT / "derived-index/baselines" / f"{suite_id}.json"
        output_path.unlink(missing_ok=True)

        with tempfile.TemporaryDirectory() as tmp:
            pack = Path(tmp) / "pack.yaml"
            pack.write_text(
                "\n".join(["suites:", f"  - {suite_id}", ""]),
                encoding="utf-8",
            )

            try:
                result = subprocess.run(
                    [
                        "bash",
                        str(ROOT / "promptops/harnesses/generate_community_baselines.sh"),
                        str(pack),
                    ],
                    cwd=ROOT,
                    env={**os.environ, "PYTHON": sys.executable},
                    capture_output=True,
                    text=True,
                    check=False,
                )

                self.assertEqual(result.returncode, 0, msg=result.stdout + result.stderr)
                self.assertTrue(output_path.exists())
            finally:
                output_path.unlink(missing_ok=True)

    @unittest.skipUnless(shutil.which("npx"), "npx is required for run script checks")
    def test_establish_baseline_uses_portable_tempfile(self):
        suite_id = f"test-portable-{uuid.uuid4().hex}"
        baseline_name = "baseline"
        output_path = ROOT / "derived-index/baselines" / f"{suite_id}-{baseline_name}.json"
        output_path.unlink(missing_ok=True)

        try:
            result = subprocess.run(
                [
                    "bash",
                    str(ROOT / "promptops/runs/establish_baseline.sh"),
                    suite_id,
                    baseline_name,
                    "sha256:" + ("a" * 64),
                ],
                cwd=ROOT,
                capture_output=True,
                text=True,
                check=False,
            )

            self.assertEqual(result.returncode, 0, msg=result.stdout + result.stderr)
            self.assertTrue(output_path.exists())
        finally:
            output_path.unlink(missing_ok=True)

    @unittest.skipUnless(shutil.which("npx"), "npx is required for run script checks")
    def test_generate_regression_report_uses_portable_tempfile(self):
        report_id = f"test-portable-{uuid.uuid4().hex}"
        output_path = ROOT / "derived-index/regressions" / f"{report_id}.json"
        output_path.unlink(missing_ok=True)

        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            candidate = tmp_path / "candidate.json"
            baseline = tmp_path / "baseline.json"
            policy = tmp_path / "policy.yaml"

            candidate.write_text(
                json.dumps(
                    {
                        "normalized_metrics": {"exact_match": 0.9},
                        "total_cost": 0.2,
                    }
                ),
                encoding="utf-8",
            )
            baseline.write_text(
                json.dumps(
                    {
                        "normalized_metrics": {"exact_match": 0.85},
                        "total_cost": 0.1,
                    }
                ),
                encoding="utf-8",
            )
            policy.write_text(
                "\n".join(
                    [
                        "baseline: prod current",
                        "rules:",
                        "  - metric: exact_match",
                        "    floor: 0.8",
                        "    allowed_delta: 0.05",
                        "    direction: higher_is_better",
                        "    severity: blocker",
                        "",
                    ]
                ),
                encoding="utf-8",
            )

            try:
                env = {**os.environ, "PYTHON": sys.executable}
                result = subprocess.run(
                    [
                        "bash",
                        str(ROOT / "promptops/runs/generate_regression_report.sh"),
                        str(candidate),
                        str(baseline),
                        str(policy),
                        report_id,
                    ],
                    cwd=ROOT,
                    env=env,
                    capture_output=True,
                    text=True,
                    check=False,
                )

                self.assertEqual(result.returncode, 0, msg=result.stdout + result.stderr)
                self.assertTrue(output_path.exists())
            finally:
                output_path.unlink(missing_ok=True)


if __name__ == "__main__":
    unittest.main()
