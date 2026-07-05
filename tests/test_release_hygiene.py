import re
import subprocess
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
FORBIDDEN_TRACKED_PATH = re.compile(
    r"(^|/)(__pycache__|.*\.pyc|.*\.orig|.*\.rej|\.DS_Store)$"
)


class ReleaseHygieneTests(unittest.TestCase):
    def test_no_generated_or_patch_artifact_files_are_tracked(self):
        result = subprocess.run(
            ["git", "ls-files"],
            cwd=ROOT,
            capture_output=True,
            text=True,
            check=True,
        )
        offenders = [
            path
            for path in result.stdout.splitlines()
            if FORBIDDEN_TRACKED_PATH.search(path)
        ]

        self.assertEqual(offenders, [])

    def test_github_workflows_do_not_depend_on_yq(self):
        workflow_paths = [
            *sorted((ROOT / ".github/workflows").glob("*.yml")),
            *sorted((ROOT / "setup-ci/templates/.github/workflows").glob("*.yml")),
        ]
        offenders = [
            str(path.relative_to(ROOT))
            for path in workflow_paths
            if re.search(r"\byq\b", path.read_text(encoding="utf-8"))
        ]

        self.assertEqual(offenders, [])


if __name__ == "__main__":
    unittest.main()
