import argparse
from copy import deepcopy
import json
from pathlib import Path
import shlex
import shutil
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

from promptops.runtime.digest import compute_digest_from_dict, dataset_digest
from promptops.runtime.quick import build_quick_request


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "promptops/harnesses/promptfoo/run.py"
PROMPTFOO = ROOT / "node_modules/.bin/promptfoo"


def request_fixture(directory, models=None, trials=2):
    path = Path(directory) / "quick.json"
    path.write_text(json.dumps({"id": "real-response", "prompt": "{{text}}", "cases": [{"case_id": "first", "inputs": {"text": "hello"}, "assert": [{"type": "equals", "value": "HELLO"}]}, {"case_id": "second", "inputs": {"text": "bye"}, "assert": [{"type": "contains", "value": "BY"}]}], "thresholds": {"pass_rate": 1}}))
    request = build_quick_request(path, models or ["test:one", "test:two"])
    request["trials"] = request["suite"]["trials"] = trials
    request["suite_digest"] = compute_digest_from_dict(request["suite"])
    return request


def exported_rows(request, model):
    from promptops.harnesses.promptfoo.run import build_config
    config = build_config(request, model)
    return [{"testIdx": index, "promptIdx": 0, "provider": {"id": model, "label": model}, "testCase": test, "vars": test["vars"], "prompt": {"raw": test["vars"]["apastra_rendered_prompt"]}, "response": {"output": test["vars"]["apastra_rendered_prompt"].upper(), "cached": False, "cost": 0}, "cost": 0, "success": True} for index, test in enumerate(config["tests"])]


class PromptfooProtocolTests(unittest.TestCase):
    def test_sample_descriptor_pins_the_declared_script(self):
        from promptops.runtime.adapter_identity import implementation_identity
        from promptops.runtime.digest import load_asset
        from promptops.runtime.suite import validate_asset
        path = SCRIPT.with_name("adapter.yaml")
        descriptor = load_asset(path)
        validate_asset(descriptor, "harness-adapter")
        self.assertEqual(implementation_identity(path, descriptor)["mode"], "pinned_files")
        self.assertEqual(set(descriptor["implementation"]["files"]), {"run.py"})

    def test_config_expands_trials_once_and_scores_actual_responses(self):
        from promptops.harnesses.promptfoo.run import build_config, parse_results
        with tempfile.TemporaryDirectory() as directory:
            request = request_fixture(directory)
            config = build_config(request, "test:one")
            self.assertEqual(len(config["tests"]), 4)
            self.assertEqual(config["evaluateOptions"]["repeat"], 1)
            self.assertFalse(config["evaluateOptions"]["cache"])
            rows = exported_rows(request, "test:one")
            cases, cost = parse_results(request, "test:one", rows)
            self.assertEqual(cost, 0)
            self.assertEqual(len(cases), 2)
            self.assertEqual(cases[0]["per_trial_outputs"][0]["evaluator_outputs"], {"pass_rate": 1.0})
            rows[0]["response"]["output"] = "wrong response"
            cases, _ = parse_results(request, "test:one", rows)
            self.assertEqual(cases[0]["per_trial_outputs"][0]["evaluator_outputs"], {"pass_rate": 0.0})

    def test_incomplete_duplicate_stale_wrong_model_and_provider_errors_fail(self):
        from promptops.harnesses.promptfoo.run import parse_results
        with tempfile.TemporaryDirectory() as directory:
            request = request_fixture(directory)
            valid = exported_rows(request, "test:one")
            variants = [valid[:-1], valid + [valid[0]]]
            for field, value in (("testIdx", 100), ("promptIdx", 1), ("success", False), ("error", "provider error")):
                rows = deepcopy(valid)
                rows[0][field] = value
                variants.append(rows)
            for change in (lambda row: row["provider"].update(label="test:two"), lambda row: row["testCase"]["metadata"].update(apastra_trial_id=99), lambda row: row["response"].update(cached=True), lambda row: row["response"].update(error="failed"), lambda row: row["prompt"].update(raw="different input"), lambda row: row["response"].update(output={"unexpected": "object"}), lambda row: row.update(cost=-1), lambda row: row.update(provider="bad"), lambda row: row.update(testCase="bad"), lambda row: row.update(prompt="bad"), lambda row: row["response"].update(error=None)):
                rows = deepcopy(valid)
                change(rows[0])
                variants.append(rows)
            for rows in variants:
                with self.subTest(rows=rows[0].get("testIdx")), self.assertRaises(ValueError):
                    parse_results(request, "test:one", rows)

    def test_cost_overflow_and_unsafe_output_directory_fail(self):
        from promptops.harnesses.promptfoo.run import execute, parse_results
        with tempfile.TemporaryDirectory() as directory:
            request = request_fixture(directory)
            rows = exported_rows(request, "test:one")
            for row in rows:
                row["cost"] = row["response"]["cost"] = 1e308
            with self.assertRaises(ValueError):
                parse_results(request, "test:one", rows)
            request_path = Path(directory) / "request.json"
            request_path.write_text(json.dumps(request))
            unsafe = Path(directory) / "unsafe"
            unsafe.symlink_to(directory, target_is_directory=True)
            with self.assertRaises(ValueError):
                execute(request_path, unsafe, "must-not-execute")

    def test_unsupported_evaluator_sampling_and_assertions_fail_before_execution(self):
        from promptops.harnesses.promptfoo.run import validate_supported_request
        with tempfile.TemporaryDirectory() as directory:
            request = request_fixture(directory)
            validate_supported_request(request)
            variants = []
            changed = deepcopy(request)
            changed["harness_version"] = "2.0.0"
            variants.append(changed)
            changed = deepcopy(request)
            changed["sampling_config"] = changed["suite"]["sampling_config"] = {"temperature": 0.7}
            changed["suite_digest"] = compute_digest_from_dict(changed["suite"])
            variants.append(changed)
            changed = deepcopy(request)
            changed["evaluators"][0]["id"] = "another-evaluator"
            changed["evaluator_refs"] = changed["suite"]["evaluators"] = ["another-evaluator"]
            changed["evaluator_digest"] = compute_digest_from_dict(changed["evaluators"][0])
            changed["suite_digest"] = compute_digest_from_dict(changed["suite"])
            variants.append(changed)
            for kind in ("llm-rubric", "latency", "similar", "cost"):
                changed = deepcopy(request)
                changed["cases"][0]["assert"] = [{"type": kind, "value": "unsupported"}]
                changed["dataset_digest"] = dataset_digest(changed["cases"])
                variants.append(changed)
            for changed in variants:
                with self.assertRaises(ValueError):
                    validate_supported_request(changed)

    def test_deterministic_assertions_and_invalid_assertion_values(self):
        from promptops.harnesses.promptfoo.run import score_assertions
        for kind, value in (("equals", "Hello"), ("contains", "ell"), ("icontains", "HEL"), ("contains-any", ["absent", "ell"]), ("contains-all", ["He", "lo"]), ("regex", "^H.*o$"), ("starts-with", "He")):
            with self.subTest(kind=kind):
                self.assertEqual(score_assertions([{"type": kind, "value": value}], "Hello"), 1)
                self.assertEqual(score_assertions([{"type": "not-" + kind, "value": value}], "Hello"), 0)
        self.assertEqual(score_assertions([{"type": "is-json"}], '{"a":1}'), 1)
        self.assertEqual(score_assertions([{"type": "is-valid-json-schema", "value": {"type": "object", "required": ["a"]}}], '{"a":1}'), 1)
        for assertion in ({"type": "regex", "value": "["}, {"type": "contains", "value": 12}, {"type": "is-valid-json-schema", "value": {"type": "invalid"}}, {"type": "equals", "value": "ok", "threshold": 0.1}, {"type": "is-valid-json-schema", "value": {"$ref": "https://invalid.example/schema"}}):
            with self.assertRaises(ValueError):
                score_assertions([assertion], "Hello")


    def test_builtin_evaluator_errors_and_nonnumeric_results_do_not_score(self):
        from promptops.harnesses.promptfoo.run import score_assertions
        for results in ([], [{"status": "error"}], [{"assert_equals": None}], [{"assert_equals": float("nan")}], [{"assert_equals": True}], [{"assert_equals": 0.5}]):
            with patch("promptops.harnesses.promptfoo.run.evaluate_assertions", return_value=results), self.assertRaises(ValueError):
                score_assertions([{"type": "equals", "value": "ok"}], "ok")

    def test_assertions_use_the_existing_evaluator_semantics(self):
        from promptops.harnesses.promptfoo.run import score_assertions
        from promptops.runs.evaluate_assertions import evaluate_assertions
        examples = [
            ("prose ```json\n{\"a\": 1}\n``` end", {"type": "is-valid-json-schema", "value": {"type": "object", "required": ["a"]}}),
            ("42", {"type": "contains-json"}),
            ("Straße", {"type": "icontains", "value": "STRASSE"}),
            ('{\"a\": 1, \"a\": 2}', {"type": "is-json"}),
        ]
        for output, assertion in examples:
            for negate in (False, True):
                current = {**assertion, "type": ("not-" if negate else "") + assertion["type"]}
                expected = evaluate_assertions(output, [current])[0]["assert_" + current["type"]]
                with self.subTest(assertion=current, output=output):
                    self.assertEqual(score_assertions([current], output), expected)



class PromptfooInstalledIntegrationTests(unittest.TestCase):
    def test_actual_promptfoo_python_provider_admits_measured_coverage_and_quality(self):
        if not PROMPTFOO.is_file():
            self.skipTest("Pass --promptfoo-executable to run the real pinned CLI integration")
        from promptops.runtime.gate import admit_run
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            provider = root / "provider.py"
            provider.write_text('def call_api(prompt, options, context):\n    return {"output": prompt.upper(), "cost": 0}\n')
            second_provider = root / "second_provider.py"
            second_provider.write_text(provider.read_text())
            models = ["file://" + str(provider), "file://" + str(second_provider)]
            request = request_fixture(root, models)
            adapter = root / "adapter.json"
            adapter.write_text(json.dumps({"id": "promptfoo", "type": "harness_adapter", "version": "1.0.0", "execution_mode": "measured", "capabilities": ["run_suite", "model_matrix", "trials"], "entrypoint": shlex.join([sys.executable, str(SCRIPT), "--promptfoo-executable", str(PROMPTFOO)])}))
            home = root / "isolated-home"
            home.mkdir()
            child = {"PATH": str(Path(sys.executable).parent) + ":/opt/homebrew/bin:/usr/local/bin:/usr/bin:/bin", "HOME": str(home), "PROMPTFOO_CONFIG_DIR": str(home / "config"), "PROMPTFOO_PYTHON": sys.executable, "PROMPTFOO_DISABLE_TELEMETRY": "1", "PROMPTFOO_DISABLE_UPDATE": "1", "CI": "1"}
            def run_actual(data, destination):
                request_path = root / "request.json"
                request_path.write_text(json.dumps(data))
                result = subprocess.run([sys.executable, "-B", "-m", "promptops.runtime.runner", str(request_path), str(adapter), str(destination)], cwd=ROOT, env=child, capture_output=True, text=True, timeout=60)
                if result.stdout.strip():
                    return json.loads(result.stdout)
                return {"status": "error", "exit_code": result.returncode}
            output = root / "output"
            decision = run_actual(request, output)
            self.assertEqual(decision["status"], "pass")
            self.assertEqual(admit_run(output, adapter)["decision"]["metrics"], {"pass_rate": 1})
            rows = [json.loads(line) for line in (output / "cases.jsonl").read_text().splitlines()]
            self.assertEqual(len(rows), 4)
            self.assertEqual({row["model_id"] for row in rows}, set(models))
            self.assertTrue(all(len(row["per_trial_outputs"]) == 2 for row in rows))
            self.assertTrue((output / "promptfoo/model-1.jsonl").is_file())
            raw = output / "promptfoo/model-1.jsonl"
            original = raw.read_text()
            raw.write_text(original + "\n")
            with self.assertRaisesRegex(ValueError, "reference"):
                admit_run(output, adapter)
            raw.write_text(original)
            installed_cli = root / ".agent/bin/apastra"
            installed_cli.parent.mkdir(parents=True)
            installed_cli.write_text((ROOT / "bin/apastra").read_text())
            shutil.copytree(ROOT / "promptops", root / ".agent/scripts/apastra", ignore=shutil.ignore_patterns("__pycache__"))
            installed_config = root / "promptops/harnesses/promptfoo.json"
            installed_config.parent.mkdir(parents=True)
            configuration = json.loads(adapter.read_text())
            configuration["entrypoint"] = shlex.join(["python3", ".agent/scripts/apastra/harnesses/promptfoo/run.py", "--promptfoo-executable", str(PROMPTFOO)])
            installed_config.write_text(json.dumps(configuration))
            installed_output = root / "installed-output"
            result = subprocess.run([sys.executable, "-B", str(installed_cli), "quick-eval", str(root / "quick.json"), "--models", *models, "--adapter", str(installed_config), "--output-dir", str(installed_output)], cwd=root, env=child, capture_output=True, text=True, timeout=60)
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertEqual(json.loads(result.stdout)["status"], "pass")
            self.assertEqual(admit_run(installed_output, installed_config)["decision"]["status"], "pass")
            self.assertEqual(run_actual(request, output)["status"], "error")
            provider.write_text('def call_api(prompt, options, context):\n    return {"output": "incorrect", "cost": 0}\n')
            self.assertEqual(run_actual(request, root / "quality-fail")["status"], "fail")
            provider.write_text('def call_api(prompt, options, context):\n    return {"error": "intentional provider failure"}\n')
            result = run_actual(request, root / "provider-fail")
            self.assertEqual(result["status"], "error")
            self.assertFalse((root / "provider-fail/scorecard.json").exists())
            broken = request_fixture(root, ["apastra-unknown:missing"], trials=1)
            self.assertEqual(run_actual(broken, root / "unknown-provider")["status"], "error")
            self.assertFalse((root / "unknown-provider/scorecard.json").exists())


if __name__ == "__main__":
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument("--promptfoo-executable", default=str(PROMPTFOO))
    options, remaining = parser.parse_known_args()
    PROMPTFOO = Path(options.promptfoo_executable).resolve()
    unittest.main(argv=[sys.argv[0], *remaining])
