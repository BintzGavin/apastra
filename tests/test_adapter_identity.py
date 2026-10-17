import contextlib
import hashlib
import json
from pathlib import Path
import shlex
import sys
import tempfile
import unittest

from tests.test_evaluation_contract import HARNESS, make_workspace


def raw_digest(path):
    return "sha256:" + hashlib.sha256(path.read_bytes()).hexdigest()


class AdapterIdentityTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.workspace, self.adapter = make_workspace(temporary.name)
        self.base = self.adapter.parent
        self.target = self.base / "target.py"
        self.target.write_text(HARNESS.read_text())
        self.helper = self.base / "helper.txt"
        self.helper.write_text("declared dependency\n")
        self.config = json.loads(self.adapter.read_text())
        self.config["entrypoint"] = shlex.join([sys.executable, str(self.target), "valid"])

    def pin(self, files=None):
        self.config["implementation"] = {"files": files if files is not None else {"target.py": raw_digest(self.target), "helper.txt": raw_digest(self.helper)}}
        self.adapter.write_text(json.dumps(self.config))

    def execute(self, name="evidence"):
        from promptops.runtime.runner import run
        from promptops.runtime.suite import build_request
        with contextlib.chdir(self.workspace):
            return run(build_request("demo"), self.adapter, self.workspace / name)

    def test_given_no_file_pins_when_running_then_identity_explicitly_says_configuration_only(self):
        from promptops.runtime.gate import admit_run
        self.adapter.write_text(json.dumps(self.config))
        self.assertEqual(self.execute()["status"], "pass")
        invocation = json.loads((self.workspace / "evidence/invocation.json").read_text())
        self.assertEqual(invocation["implementation_identity"], {"mode": "configuration_only"})
        self.assertEqual(admit_run(self.workspace / "evidence", self.adapter)["decision"]["status"], "pass")

    def test_given_file_pins_when_running_then_canonical_mapping_digest_is_recorded(self):
        from promptops.runtime.digest import compute_digest_from_dict
        from promptops.runtime.gate import admit_run
        self.pin()
        self.assertEqual(self.execute()["status"], "pass")
        invocation = json.loads((self.workspace / "evidence/invocation.json").read_text())
        expected = {"mode": "pinned_files", "digest": compute_digest_from_dict(self.config["implementation"]["files"])}
        self.assertEqual(invocation["implementation_identity"], expected)
        self.pin(dict(reversed(list(self.config["implementation"]["files"].items()))))
        self.assertEqual(admit_run(self.workspace / "evidence", self.adapter)["decision"]["status"], "pass")

    def test_given_changed_or_missing_pinned_file_when_running_then_harness_never_runs(self):
        for variant in ("changed", "missing"):
            with self.subTest(variant=variant):
                self.helper.write_text("initial")
                self.pin()
                if variant == "changed":
                    self.helper.write_text("altered")
                else:
                    self.helper.unlink()
                with self.assertRaisesRegex(ValueError, "implementation"):
                    self.execute(variant)
                self.assertFalse((self.workspace / variant / "run_manifest.json").exists())

    def test_given_unsafe_pin_paths_when_running_then_execution_is_rejected(self):
        link = self.base / "linked.txt"
        link.symlink_to(self.helper)
        nested = self.base / "nested"
        nested.symlink_to(self.base, target_is_directory=True)
        for index, name in enumerate(("linked.txt", "nested/helper.txt", "../helper.txt", str(self.helper), "./helper.txt", "helper.txt/", "helper.txt\\other")):
            with self.subTest(name=name):
                self.pin({name: raw_digest(self.helper)})
                with self.assertRaises(ValueError):
                    self.execute(str(index))
                self.assertFalse((self.workspace / str(index) / "run_manifest.json").exists())

    def test_given_harness_mutates_pinned_file_when_finished_then_evidence_is_not_admitted(self):
        self.target.write_text(HARNESS.read_text() + "\nPath(__file__).with_name('helper.txt').write_text('changed during execution')\n")
        self.pin()
        with self.assertRaisesRegex(ValueError, "implementation"):
            self.execute()
        self.assertTrue((self.workspace / "evidence/run_manifest.json").is_file())
        self.assertFalse((self.workspace / "evidence/evaluation.json").exists())

    def test_given_file_changes_after_execution_when_admitting_then_readback_rejects(self):
        from promptops.runtime.gate import admit_run
        self.pin()
        self.execute()
        self.helper.write_text("changed after execution")
        with self.assertRaisesRegex(ValueError, "implementation"):
            admit_run(self.workspace / "evidence", self.adapter)

    def test_given_implementation_identity_tampering_when_admitting_then_producer_is_rejected(self):
        from promptops.runtime.gate import admit_run
        self.pin()
        self.execute()
        path = self.workspace / "evidence/invocation.json"
        invocation = json.loads(path.read_text())
        invocation["implementation_identity"] = {"mode": "configuration_only"}
        path.write_text(json.dumps(invocation))
        with self.assertRaisesRegex(ValueError, "producer"):
            admit_run(self.workspace / "evidence", self.adapter)

    def test_given_mutation_and_process_failure_when_finished_then_pins_are_still_checked(self):
        self.target.write_text(HARNESS.read_text() + "\nPath(__file__).with_name('helper.txt').write_text('changed')\nraise SystemExit(7)\n")
        self.pin()
        with self.assertRaisesRegex(ValueError, "implementation"):
            self.execute()
        self.assertFalse((self.workspace / "evidence/invocation.json").exists())

    def test_given_changed_pin_set_or_mode_when_regressing_then_inputs_are_rejected(self):
        from promptops.runtime.gate import regression
        policy = {"baseline": "prod", "rules": [{"metric": "exact_match_score", "allowed_delta": 0, "direction": "higher_is_better", "severity": "blocker"}]}
        self.adapter.write_text(json.dumps(self.config))
        self.execute("configuration-only")
        self.pin()
        self.execute("pinned-first")
        with self.assertRaisesRegex(ValueError, "producer"):
            regression(self.workspace / "pinned-first", self.workspace / "configuration-only", policy, self.adapter)
        self.helper.write_text("new declared implementation")
        self.pin()
        self.execute("pinned-second")
        with self.assertRaisesRegex(ValueError, "producer"):
            regression(self.workspace / "pinned-second", self.workspace / "pinned-first", policy, self.adapter)

    def test_given_invalid_pin_declaration_when_running_then_schema_rejects(self):
        for index, declaration in enumerate(({}, {"files": {}}, {"files": {"helper.txt": "not-a-digest"}}, {"files": {"helper.txt": raw_digest(self.helper)}, "unknown": True})):
            with self.subTest(declaration=declaration):
                self.config["implementation"] = declaration
                self.adapter.write_text(json.dumps(self.config))
                with self.assertRaisesRegex(ValueError, "harness-adapter"):
                    self.execute(str(index))
