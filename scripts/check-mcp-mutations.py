"""Targeted security/verdict mutants in disposable copies; no workspace edits."""
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[1]
AUTH = "tests.test_mcp_transport.TransportTests.test_verifier_rejects_wrong_owner_audience_issuer_expiry_and_signature"
WORKFLOW = "tests.test_mcp_workflow.WorkflowTests."
MUTANTS = [
    ("owner binding removed", "promptops/runtime/mcp_auth.py", [('claims["sub"] != self.subject or ', '')], AUTH),
    ("audience validation removed", "promptops/runtime/mcp_auth.py", [('options={"require":', 'options={"verify_aud": False, "require":')], AUTH),
    ("scope restriction removed", "promptops/runtime/mcp_auth.py", [('if "apastra:evaluate" not in scopes:', 'if False:')], AUTH),
    ("path confinement removed", "promptops/runtime/mcp_workflow.py", [('if not path.resolve().is_relative_to(root) or any(part.is_symlink() for part in (path, *path.parents) if part != root and part.is_relative_to(root)):', 'if False:')], WORKFLOW + "test_workspace_and_output_symlinks_are_rejected"),
    ("config comparability removed", "promptops/runtime/gate.py", [('if candidate["request"][field] != baseline["request"][field]:', 'if False:'), ('if field not in {"prompt", "name", "description"} and candidate["request"]["suite"].get(field) != baseline["request"]["suite"].get(field):', 'if False:')], WORKFLOW + "test_changed_cases_and_config_are_inconclusive"),
    ("regression always reported", "promptops/runtime/mcp_workflow.py", [('worse = any(row["status"] == "fail" for row in report["evidence"])', 'worse = True')], WORKFLOW + "test_complete_candidate_baseline_and_inspectable_evidence"),
    ("failing baseline allowed", "promptops/runtime/gate.py", [('if baseline["decision"]["status"] != "pass":', 'if False:')], "tests.test_mcp_workflow.DemoTests.test_prompt_regression_and_fix_with_same_cases_and_model"),
]

def check(directory, test):
    script = "import io,json,unittest,sys; suite=unittest.defaultTestLoader.loadTestsFromNames(json.loads(sys.argv[1])); r=unittest.TextTestRunner(stream=io.StringIO()).run(suite); print(json.dumps({'tests':r.testsRun,'failures':len(r.failures),'errors':len(r.errors)}))"
    completed = subprocess.run([sys.executable, "-B", "-c", script, json.dumps(test)], cwd=directory, capture_output=True, text=True, timeout=60)
    if completed.returncode:
        raise RuntimeError("Mutation test process failed")
    return json.loads(completed.stdout)


def main():
    report = []
    with tempfile.TemporaryDirectory(prefix="apastra-mcp-mutants-") as directory:
        root = Path(directory)
        for name in ("promptops", "tests", "bin"):
            shutil.copytree(ROOT / name, root / name, ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))
        baseline = check(root, sorted({row[3] for row in MUTANTS}))
        if baseline["failures"] or baseline["errors"]:
            raise RuntimeError("Unchanged mutation baseline must pass")
        for name, relative, changes, test in MUTANTS:
            path = root / relative
            original = path.read_text()
            changed = original
            for before, after in changes:
                if before not in changed:
                    raise RuntimeError("Mutation target drifted: " + name)
                changed = changed.replace(before, after, 1)
            try:
                path.write_text(changed)
                result = check(root, [test])
            finally:
                path.write_text(original)
            status = "killed" if result["failures"] and not result["errors"] else "invalid" if result["errors"] else "survived"
            report.append({"mutation": name, "status": status, **result})
    print(json.dumps(report, indent=2))
    return 0 if all(row["status"] == "killed" for row in report) else 1


if __name__ == "__main__":
    raise SystemExit(main())
