"""Run targeted trust mutants in disposable copies, never the working tree."""

import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile


ROOT = Path(__file__).resolve().parents[1]
EXECUTION = "tests.test_evaluation_contract.EvaluationExecutionTests."
GATE = "tests.test_gate_contract.GateContractTests."
MUTANTS = [
    ("missing adapter passes", "promptops/runtime/compare.py", [("raise ValueError(\"An evaluation adapter is required\")", 'return {"status": "pass"}')], "tests.test_runtime_integrity.RuntimeIntegrityTests.test_missing_adapter_cannot_create_a_scorecard"),
    ("fixture evidence passes", "promptops/runtime/evidence.py", [('if manifest.get("execution_mode") != "measured":', 'if False:')], EXECUTION + "test_zero_exit_does_not_make_empty_or_invalid_evidence_successful"),
    ("empty coverage passes", "promptops/runtime/evidence.py", [("if seen != expected:", "if False:"), ("mean = math.fsum(measured) / len(measured)", "mean = math.fsum(measured) / len(measured) if measured else metrics[name]")], EXECUTION + "test_zero_exit_does_not_make_empty_or_invalid_evidence_successful"),
    ("errors become scores", "promptops/runs/evaluate_assertions.py", [('results.append({"status": "error", "assertion": kind, "reason": reason})', 'results.append({"assert_" + kind: 1.0})')], "tests.test_evaluate_assertions.EvaluateAssertionsTests.test_negation_never_turns_an_evaluator_error_into_a_pass"),
    ("missing cost becomes zero", "promptops/runtime/evidence.py", [('cost = manifest.get("total_cost")', 'cost = manifest.get("total_cost", 0)')], EXECUTION + "test_cost_budget_needs_a_measurement_and_accepts_real_zero"),
    ("manifest digest mismatch ignored", "promptops/runtime/evidence.py", [('if not request.get(name) or manifest.get("resolved_digests", {}).get(name) != request[name]:', 'if False:')], EXECUTION + "test_zero_exit_does_not_make_empty_or_invalid_evidence_successful"),
    ("model mismatch ignored", "promptops/runtime/evidence.py", [('if not models or len(set(models)) != len(models) or manifest.get("model_ids") != models:', 'if False:')], EXECUTION + "test_zero_exit_does_not_make_empty_or_invalid_evidence_successful"),
    ("empty policy passes", "promptops/schemas/regression-policy.schema.json", [('"minItems": 1', '"minItems": 0')], GATE + "test_policy_is_nonempty_typed_and_cannot_waive_flakes"),
    ("stale revision admitted", "promptops/runtime/gate.py", [(' or request.get("source_revision") != expected_revision', '')], GATE + "test_stored_evidence_checks_producer_revision_and_content"),
    ("comparison budget is per model", "promptops/runtime/compare.py", [('if cost_budget is not None and (model not in costs or math.fsum(costs.values()) > cost_budget):', 'if False:')], "tests.test_evaluation_contract.SuiteExecutionTests.test_comparison_cannot_split_its_way_around_the_suite_cost_budget"),
]


def run_tests(directory, tests, home):
    script = "import io,json,unittest; names=json.loads(__import__('sys').argv[1]); suite=unittest.TestSuite(unittest.defaultTestLoader.loadTestsFromName(name) for name in names); result=unittest.TextTestRunner(stream=io.StringIO()).run(suite); print(json.dumps({'tests':result.testsRun,'failures':len(result.failures),'errors':len(result.errors)}))"
    completed = subprocess.run([sys.executable, "-B", "-c", script, json.dumps(tests)], cwd=directory,
                               env={"PATH": "/opt/homebrew/bin:/usr/local/bin:/usr/bin:/bin", "HOME": str(home), "PYTHON": sys.executable},
                               capture_output=True, text=True, timeout=60)
    if completed.returncode:
        raise RuntimeError("Mutation process could not run its tests")
    return json.loads(completed.stdout)


def main():
    report = {"mutants": []}
    with tempfile.TemporaryDirectory(prefix="apastra-trust-mutants-") as temporary:
        root = Path(temporary)
        checkout = root / "checkout"
        checkout.mkdir()
        home = root / "home"
        home.mkdir()
        for name in ("promptops", "tests", "bin"):
            shutil.copytree(ROOT / name, checkout / name, ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))
        tests = sorted({entry[3] for entry in MUTANTS})
        report["baseline"] = run_tests(checkout, tests, home)
        if report["baseline"]["failures"] or report["baseline"]["errors"]:
            raise RuntimeError("Passing unchanged baseline is required before mutation testing")
        for name, relative, edits, test in MUTANTS:
            path = checkout / relative
            original = path.read_text()
            changed = original
            for before, after in edits:
                if before not in changed:
                    raise RuntimeError(f"Mutation target drifted: {name}")
                changed = changed.replace(before, after, 1)
            try:
                path.write_text(changed)
                result = run_tests(checkout, [test], home)
            finally:
                path.write_text(original)
            status = "killed" if result["failures"] and not result["errors"] else "invalid" if result["errors"] else "survived"
            report["mutants"].append({"name": name, "status": status, **result})
    print(json.dumps(report, indent=2))
    return 0 if all(row["status"] == "killed" for row in report["mutants"]) else 1


if __name__ == "__main__":
    raise SystemExit(main())
