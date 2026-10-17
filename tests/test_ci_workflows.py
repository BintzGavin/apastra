import contextlib
import json
import io
import shutil
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest import mock

from tests.test_evaluation_contract import make_workspace

ROOT = Path(__file__).resolve().parents[1]


class WorkflowGateTests(unittest.TestCase):
    def commit(self, workspace):
        for command in (["git", "init", "-q"], ["git", "add", "."], ["git", "-c", "user.name=Test", "-c", "user.email=test@example.invalid", "-c", "commit.gpgsign=false", "commit", "-qm", "test"]):
            subprocess.run(command, cwd=workspace, check=True, capture_output=True)
        return subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=workspace, text=True).strip()

    def workspace(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        workspace, _ = make_workspace(temporary.name)
        base = self.commit(workspace)
        path = workspace / "promptops/evaluators/exact.json"
        data = json.loads(path.read_text())
        data["metric_definitions"]["exact_match_score"]["version"] = "1.1.0"
        path.write_text(json.dumps(data))
        return workspace, base, self.commit(workspace)

    def gate(self, workspace, base, revision, **overrides):
        from promptops.runtime.ci_workflow import workflow_gate
        options = dict(suite="demo", adapter="promptops/harnesses/local.json", mode="evidence", run_dir="evidence/{revision}/candidate")
        options.update(overrides)
        with contextlib.chdir(workspace):
            return workflow_gate(base, revision, **options)

    def execute(self, workspace, revision):
        from promptops.runtime.ci import ci_gate
        with contextlib.chdir(workspace):
            self.assertEqual(ci_gate("demo", "promptops/harnesses/local.json", revision, "execute", f"evidence/{revision}/candidate")["status"], "pass")

    def test_evaluator_change_needs_configuration_and_evidence(self):
        workspace, base, revision = self.workspace()
        for options in ({}, {"suite": ""}, {"adapter": ""}, {"mode": ""}, {"run_dir": ""}, {"baseline": "one"}, {"policy": "one"}):
            with self.subTest(options=options), self.assertRaises(ValueError):
                self.gate(workspace, base, revision, **options)

    def test_revision_bound_evidence_passes_and_stale_or_wrong_suite_fails(self):
        workspace, base, revision = self.workspace()
        self.execute(workspace, revision)
        self.assertEqual(self.gate(workspace, base, revision)["status"], "pass")
        for options in ({"suite": "other"}, {"run_dir": f"evidence/{base}/candidate"}, {"mode": "advisory"}):
            with self.subTest(options=options), self.assertRaises(ValueError):
                self.gate(workspace, base, revision, **options)
        (workspace / "README.md").write_text("new revision, same evaluation inputs\n")
        newer = self.commit(workspace)
        shutil.copytree(workspace / f"evidence/{revision}/candidate", workspace / f"evidence/{newer}/candidate")
        with self.assertRaisesRegex(ValueError, "revision"):
            self.gate(workspace, base, newer)

    def test_changed_evaluator_after_run_fails_workspace_admission(self):
        workspace, base, revision = self.workspace()
        self.execute(workspace, revision)
        path = workspace / "promptops/evaluators/exact.json"
        data = json.loads(path.read_text())
        data["metric_definitions"]["exact_match_score"]["version"] = "2.0.0"
        path.write_text(json.dumps(data))
        with self.assertRaisesRegex(ValueError, "workspace"):
            self.gate(workspace, base, revision)

    def test_unsafe_paths_wrong_checkout_and_missing_base_fail(self):
        workspace, base, revision = self.workspace()
        for options in ({"run_dir": f"../{revision}"}, {"run_dir": f"/tmp/{revision}"}, {"adapter": "../adapter.json"}):
            with self.subTest(options=options), self.assertRaises(ValueError):
                self.gate(workspace, base, revision, **options)
        (workspace / "outside").symlink_to("/tmp", target_is_directory=True)
        with self.assertRaises(ValueError):
            self.gate(workspace, base, revision, run_dir=f"outside/{revision}")
        for bad_base, bad_revision in (("", revision), ("--help", revision), (base, base)):
            with self.assertRaises(ValueError):
                self.gate(workspace, bad_base, bad_revision)

    def test_only_irrelevant_changes_can_skip_without_configuration(self):
        workspace, _, base = self.workspace()
        (workspace / "README.md").write_text("docs\n")
        revision = self.commit(workspace)
        result = self.gate(workspace, base, revision, suite="", adapter="", mode="", run_dir="")
        self.assertEqual(result, {"status": "pass", "reason": "No evaluation inputs changed"})

    def test_execute_mode_and_relevant_paths(self):
        from promptops.runtime.ci_workflow import relevant_change
        workspace, base, revision = self.workspace()
        self.assertEqual(self.gate(workspace, base, revision, mode="execute")["status"], "pass")
        for group in ("prompts", "datasets", "evaluators", "suites", "evals", "policies", "harnesses", "runtime", "schemas", "validators"):
            self.assertTrue(relevant_change(f"promptops/{group}/changed file.yaml"))
        self.assertTrue(relevant_change(".github/workflows/regression-gate.yml"))
        self.assertTrue(relevant_change(".agent/scripts/apastra/runtime/ci.py"))
        self.assertFalse(relevant_change("docs/example.md"))

    def test_repository_and_installed_cli_admit_the_same_evidence(self):
        workspace, base, revision = self.workspace()
        self.execute(workspace, revision)
        installed = workspace / ".agent/bin/apastra"
        installed.parent.mkdir(parents=True)
        installed.write_text((ROOT / "bin/apastra").read_text())
        shutil.copytree(ROOT / "promptops", workspace / ".agent/scripts/apastra", ignore=shutil.ignore_patterns("__pycache__"))
        for cli in (ROOT / "bin/apastra", installed):
            with self.subTest(cli=cli):
                command = [sys.executable, "-B", str(cli), "ci-workflow", "gate", "--base", base, "--revision", revision, "--suite", "demo", "--adapter", "promptops/harnesses/local.json", "--mode", "evidence", "--run-dir", "evidence/{revision}/candidate"]
                result = subprocess.run(command, cwd=workspace, capture_output=True, text=True, timeout=15)
                self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
                self.assertEqual(json.loads(result.stdout)["status"], "pass")
                result = subprocess.run(command[:command.index("--suite")], cwd=workspace, capture_output=True, text=True, timeout=15)
                self.assertNotEqual(result.returncode, 0)

    def test_deleted_input_is_relevant_and_unknown_base_fails(self):
        workspace, _, base = self.workspace()
        (workspace / "promptops/evaluators/exact.json").unlink()
        revision = self.commit(workspace)
        with self.assertRaises(ValueError):
            self.gate(workspace, base, revision, suite="")
        with self.assertRaises(ValueError):
            self.gate(workspace, "f" * 40, revision)

    def test_given_product_code_config_or_install_change_then_gate_is_required(self):
        from promptops.runtime.ci_workflow import relevant_change
        relevant = (
            "promptops/resolver/chain.py", "promptops/runs/evaluate_assertions.py",
            "promptops/hooks/agent_hook.py", "promptops/hooks/schema_validator.js",
            "promptops/request_log/gateway.py", "promptops/integrations/kody/apastra/client.ts",
            "promptops/manifests/consumption-example.yaml", "promptops/baselines/prod.json",
            "derived-index/baselines/demo-prod.json", "pyproject.toml", "setup.cfg",
            "scripts/install.py", "setup", "postinstall.sh", "package.json", "package-lock.json",
            "requirements.txt", "requirements-dev.txt", "uv.lock", "pnpm-lock.yaml",
            "Pipfile", ".npmrc", ".python-version", "Dockerfile",
            "promptops/extensions/worker.py", "promptops/runs/captured/target.js",
            "promptops/runs/runner-config.json", "promptops/runs/nested/policy.json",
            "promptops/datasets/tests/cases.jsonl", "promptops/evals/tests/check.yaml",
            "promptops/runtime/tests/runner.py", "promptops/resolver/tests/chain.py",
            ".agent/scripts/apastra/datasets/tests/cases.jsonl",
            ".agent/scripts/apastra/runtime/tests/runner.py", ".agent/runtime/tests/runner.py",
            ".agent/runtime/suite.py", ".agent/scripts/apastra/resolver/chain.py",
            ".agent/scripts/apastra/runs/evaluate_assertions.py", ".agent/bin/apastra",
            ".agent/apastra.config.yaml", ".github/workflows/schema-validation.yml",
        )
        irrelevant = (
            "README.md", "docs/example.md", "docs/example.yaml", "tests/test_resolver.py",
            "tests/fixtures/target.sh", "promptops/runtime/README.md",
            "promptops/runs/run-one/scorecard.json", "promptops/runs/run-one/cases.jsonl",
            "derived-index/regressions/report.json", ".agent/scripts/apastra/tests/test_suite.py",
            ".agent/scripts/apastra/runtime/README.md",
        )
        for path in relevant:
            with self.subTest(path=path):
                self.assertTrue(relevant_change(path), path)
        for path in irrelevant:
            with self.subTest(path=path):
                self.assertFalse(relevant_change(path), path)

    def test_given_only_resolver_change_when_cli_has_blank_config_then_it_cannot_skip(self):
        workspace, _, base = self.workspace()
        changed = workspace / "promptops/resolver/chain.py"
        changed.parent.mkdir()
        changed.write_text("# changed executable resolver\n")
        revision = self.commit(workspace)
        result = subprocess.run([sys.executable, "-B", str(ROOT / "bin/apastra"), "ci-workflow", "gate", "--base", base, "--revision", revision], cwd=workspace, capture_output=True, text=True, timeout=15)
        self.assertNotEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("require explicit CI", result.stderr)

    def test_given_nested_tests_asset_when_cli_has_blank_config_then_gate_cannot_skip(self):
        workspace, _, base = self.workspace()
        changed = workspace / "promptops/datasets/tests/cases.jsonl"
        changed.parent.mkdir()
        changed.write_text(json.dumps({"case_id": "nested", "inputs": {"text": "hello"}, "expected_outputs": {"text": "HELLO"}}) + "\n")
        revision = self.commit(workspace)
        result = subprocess.run([sys.executable, "-B", str(ROOT / "bin/apastra"), "ci-workflow", "gate", "--base", base, "--revision", revision], cwd=workspace, capture_output=True, text=True, timeout=15)
        self.assertNotEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("require explicit CI", result.stderr)

    def test_given_baseline_record_when_ci_resolves_it_then_run_must_stay_in_checkout(self):
        from promptops.runtime.digest import compute_digest
        from promptops.runtime.gate import establish_baseline
        workspace, base, revision = self.workspace()
        self.execute(workspace, revision)
        candidate = workspace / f"evidence/{revision}/candidate"
        policy = workspace / "policy.json"
        policy.write_text(json.dumps({"baseline": "prod", "rules": [{"metric": "exact_match_score", "allowed_delta": 0, "direction": "higher_is_better", "severity": "blocker"}]}))
        with contextlib.chdir(workspace):
            established = establish_baseline("demo", "prod", candidate, "promptops/harnesses/local.json")
        record_path = workspace / established["baseline_path"]
        record = json.loads(record_path.read_text())
        options = {"baseline": established["baseline_path"], "policy": "policy.json"}
        self.assertEqual(self.gate(workspace, base, revision, **options)["status"], "pass")
        external = tempfile.TemporaryDirectory()
        self.addCleanup(external.cleanup)
        external_run = Path(external.name) / "baseline"
        shutil.copytree(candidate, external_run)
        (workspace / "outside").symlink_to(Path(external.name), target_is_directory=True)
        for reference in (str(external_run), "../../outside/baseline"):
            with self.subTest(reference=reference):
                record_path.write_text(json.dumps({**record, "run_path": reference, "run_digest": compute_digest(external_run / "evaluation.json")}))
                with self.assertRaisesRegex(ValueError, "checkout"):
                    self.gate(workspace, base, revision, **options)


class WorkflowSchemaTests(unittest.TestCase):
    def test_flat_and_manifest_datasets_fail_closed(self):
        from promptops.runtime.ci_workflow import validate_assets
        with tempfile.TemporaryDirectory() as directory:
            workspace, _ = make_workspace(directory)
            with contextlib.chdir(workspace):
                validate_assets(["promptops/datasets/examples.jsonl"])
                (workspace / "promptops/datasets/examples.jsonl").write_text("{}\n")
                with self.assertRaises(ValueError):
                    validate_assets(["promptops/datasets/examples.jsonl"])
                manifest = workspace / "promptops/datasets/missing/manifest.json"
                manifest.parent.mkdir()
                manifest.write_text("{}")
                with self.assertRaises(ValueError):
                    validate_assets(["promptops/datasets/missing/manifest.json"])

    def test_manifest_digest_and_deleted_cases_are_checked(self):
        from promptops.runtime.ci_workflow import validate_assets
        from promptops.runtime.digest import compute_digest
        with tempfile.TemporaryDirectory() as directory:
            workspace, _ = make_workspace(directory)
            cases = workspace / "promptops/datasets/examples.jsonl"
            manifest = cases.with_name("examples.manifest.json")
            manifest.write_text(json.dumps({"id": "examples", "version": "1.0.0", "schema_version": "https://promptops.apastra.com/schemas/dataset-case.schema.json", "digest": compute_digest(cases)}))
            with contextlib.chdir(workspace):
                validate_assets(["promptops/datasets/examples.manifest.json", "promptops/datasets/examples.jsonl"])
                cases.write_text(cases.read_text().replace("hello", "bye"))
                with self.assertRaisesRegex(ValueError, "digest"):
                    validate_assets(["promptops/datasets/examples.jsonl"])
                cases.unlink()
                with self.assertRaises((ValueError, OSError)):
                    validate_assets(["promptops/datasets/examples.jsonl"])

    def test_all_evaluable_asset_kinds_are_validated(self):
        from promptops.runtime.ci_workflow import validate_assets
        for group in ("prompts", "evaluators", "suites", "evals", "policies", "harnesses"):
            with tempfile.TemporaryDirectory() as directory, self.subTest(group=group):
                path = Path(directory) / f"promptops/{group}/bad.yaml"
                path.parent.mkdir(parents=True)
                path.write_text("{}")
                with contextlib.chdir(directory), self.assertRaises(ValueError):
                    validate_assets([str(path.relative_to(directory))])

    def test_workflow_template_wiring(self):
        workflow = (ROOT / ".github/workflows/regression-gate.yml").read_text()
        self.assertEqual(workflow, (ROOT / "setup-ci/templates/.github/workflows/regression-gate.yml").read_text())
        self.assertIn("name: Regression Gate", workflow)
        self.assertIn("  gate:", workflow)
        self.assertIn("ci-workflow gate", workflow)
        self.assertNotIn("promptops-artifacts", workflow)
        self.assertNotIn("Check Regression Report Status", workflow)
        self.assertIn("ci-workflow validate-assets", (ROOT / ".github/workflows/schema-validation.yml").read_text())

    def test_given_derived_baseline_change_when_validating_assets_then_record_is_checked(self):
        from promptops.runtime.ci_workflow import validate_assets
        with tempfile.TemporaryDirectory() as directory, contextlib.chdir(directory):
            path = Path("derived-index/baselines/invalid.json")
            path.parent.mkdir(parents=True)
            path.write_text("{}")
            with self.assertRaisesRegex(ValueError, "baseline"):
                validate_assets([path.as_posix()])
            other = Path("derived-index/regressions/report.json")
            other.parent.mkdir(parents=True)
            other.write_text("{}")
            self.assertEqual(validate_assets([other.as_posix()])["validated_assets"], 0)

    def test_given_runtime_or_scoring_change_when_validating_then_all_assets_are_scanned(self):
        from promptops.runtime.ci_workflow import main
        changes = ("promptops/resolver/chain.py", "promptops/runs/evaluate_assertions.py", "promptops/hooks/schema_validator.js", ".agent/scripts/apastra/resolver/chain.py", ".agent/runtime/suite.py", "scripts/install.py", "package-lock.json")
        for changed in changes:
            with tempfile.TemporaryDirectory() as directory, self.subTest(changed=changed):
                workspace, _ = make_workspace(directory)
                invalid = workspace / "derived-index/baselines/invalid.json"
                invalid.parent.mkdir(parents=True)
                invalid.write_text("{}")
                with contextlib.chdir(workspace), mock.patch("promptops.runtime.ci_workflow.changed_paths", return_value=[changed]), contextlib.redirect_stdout(io.StringIO()):
                    with self.assertRaisesRegex(ValueError, "baseline"):
                        main(["validate-assets", "--base", "a" * 40, "--revision", "b" * 40])

    def test_schema_workflow_includes_established_baseline_records(self):
        workflow = (ROOT / ".github/workflows/schema-validation.yml").read_text()
        self.assertIn("derived-index/baselines/**", workflow)

    def test_given_consumer_baseline_asset_when_validating_then_mirrored_assets_are_checked(self):
        from promptops.runtime.ci_workflow import validate_assets
        with tempfile.TemporaryDirectory() as directory, contextlib.chdir(directory):
            path = Path(".agent/scripts/apastra/baselines/invalid.json")
            path.parent.mkdir(parents=True)
            path.write_text("{}")
            with self.assertRaisesRegex(ValueError, "baseline"):
                validate_assets([path.as_posix()])
