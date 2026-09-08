"""Create a fresh demo workspace, measure a regression and verify a fix."""
import argparse
import json
from pathlib import Path
import shutil
import sys
import time

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from promptops.runtime.mcp_workflow import EvaluationWorkspace


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("workspace", type=Path, help="New absolute directory; never overwrites an existing workspace")
    args = parser.parse_args()
    if not args.workspace.is_absolute():
        parser.error("Use an absolute path")
    shutil.copytree(Path(__file__).parent / "workspace", args.workspace)
    service = EvaluationWorkspace(args.workspace, "local-demo", "promptops/harnesses/local.json")
    def evaluate():
        run = service.start_evaluation("assistant-smoke")
        if "run_id" not in run:
            raise RuntimeError(run["reason"])
        while run["status"] in ("queued", "running"):
            time.sleep(.05)
            run = service.get_run(run["run_id"])
        if run["status"] != "completed":
            raise RuntimeError(run["reason"])
        return run["run_id"]
    prompt = args.workspace / "promptops/prompts/assistant.json"
    original = prompt.read_text()
    try:
        baseline = evaluate()
        prompt.write_text(original.replace("Uppercase", "Lowercase"))
        candidate = evaluate()
        regression = service.compare_runs(candidate, baseline)
        prompt.write_text(original)
        fixed = evaluate()
        fix = service.compare_runs(fixed, baseline)
        if regression["outcome"] != "regression" or fix["outcome"] != "success":
            raise RuntimeError("Demo did not demonstrate regression and fix")
        reference = regression["changed_cases"][0]["candidate_evidence"]["arguments"]
        print(json.dumps({"scope": "deterministic local program; no paid model evaluation", "workspace": str(args.workspace),
                          "baseline_run_id": baseline, "candidate_run_id": candidate, "fixed_run_id": fixed,
                          "regression": regression, "fix": fix, "failing_case": service.get_case(**reference)}, indent=2))
    finally:
        prompt.write_text(original)
        service.close()


if __name__ == "__main__":
    main()
