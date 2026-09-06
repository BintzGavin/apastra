import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

from promptops.runtime.digest import compute_digest
from tests.test_evaluation_contract import ROOT


class DatasetValidationTests(unittest.TestCase):
    def test_manifest_backed_dataset_works_outside_checkout_and_rejects_empty_or_stale(self):
        with tempfile.TemporaryDirectory() as directory:
            cases = Path(directory) / "cases.jsonl"
            manifest = Path(directory) / "manifest.json"
            cases.write_text('{"case_id":"one","inputs":{}}')  # Last line has no newline.
            data = {"id": "dataset", "version": "1", "schema_version": "1", "digest": compute_digest(cases)}
            manifest.write_text(json.dumps(data))
            for contents, expected in ((cases.read_text(), 0), ("", 1), ('{"case_id":"different","inputs":{}}', 1)):
                cases.write_text(contents)
                result = subprocess.run(["bash", str(ROOT / "promptops/validators/validate-dataset.sh"), str(manifest), str(cases)], cwd=directory, env={"PATH": "/usr/bin:/bin", "PYTHON": sys.executable}, capture_output=True, text=True)
                self.assertEqual(result.returncode, expected, result.stdout + result.stderr)
