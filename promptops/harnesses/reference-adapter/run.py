import sys
import json
import os
from datetime import datetime, timezone

# Import runtime resolver
# Add repo root to path to resolve promptops.runtime
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))
from promptops.runtime.resolve import resolve
# Import assertion evaluator
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../runs')))
from evaluate_assertions import evaluate_assertions


def main():
    if len(sys.argv) != 3:
        print("Usage: python run.py <run_request.json> <output_dir>")
        sys.exit(1)

    request_path = sys.argv[1]
    output_dir = sys.argv[2]

    with open(request_path, 'r') as f:
        request = json.load(f)

    os.makedirs(output_dir, exist_ok=True)

    # Resolve prompt
    revision_ref = request.get('revision_ref')
    try:
        # Just testing resolver mock
        template, metadata = resolve("mock-prompt-id", revision_ref)
        status = "success"
        failures = []
    except Exception as e:
        status = "failure"
        failures = [{"message": str(e)}]


    dataset_path = request.get('dataset_path')
    is_quick_eval = 'inline-asserts' in request.get('evaluator_refs', [])
    trials = request.get('trials', 1)

    cases_data = []
    if is_quick_eval and dataset_path and os.path.exists(dataset_path):
        with open(dataset_path, 'r') as df:
            for line in df:
                if line.strip():
                    cases_data.append(json.loads(line))

    budgets = request.get('budgets', {})
    budget_cost = budgets.get('cost', float('inf'))
    timeouts = request.get('timeouts', {})
    case_timeout = timeouts.get('time', None)  # Fallback config
    if timeouts.get('case_timeout') is not None:
        case_timeout = timeouts.get('case_timeout')
    cost_accumulated = 0.0

    # 1. Setup run_manifest.json content (written later)
    provenance = {
        "builder": {
            "id": "https://github.com/apastra/promptops/reference-adapter"
        },
        "buildType": "https://apastra.github.io/buildTypes/reference-adapter/v1",
        "invocation": {
            "configSource": {},
            "environment": {
                "GITHUB_ACTIONS": os.environ.get("GITHUB_ACTIONS", "false"),
                "GITHUB_RUN_ID": os.environ.get("GITHUB_RUN_ID", ""),
                "GITHUB_SHA": os.environ.get("GITHUB_SHA", ""),
                "USER": os.environ.get("USER", "")
            }
        },
        "metadata": {
            "buildInvocationId": os.environ.get("GITHUB_RUN_ID", "")
        }
    }

    manifest = {
        "input_refs": {
            "run_request": request_path
        },
        "resolved_digests": {
            "prompt": "sha256:dummy"
        },
        "timestamps": {
            "start": datetime.now(timezone.utc).isoformat(),
            "end": datetime.now(timezone.utc).isoformat()
        },
        "harness_version": "1.0.0",
        "model_ids": request.get("model_matrix", []),
        "environment": {
            "os": os.name
        },
        "status": status,
        "provenance": provenance
    }

    # 2. Write cases.jsonl
    cases = []
    import time
    import concurrent.futures

    def execute_case(c, trials, asserts):
        per_trial_outputs = []
        eval_outputs = []
        case_cost = 0.0
        for t in range(trials):
            mock_output = f"mock_output_{t}"
            per_trial_outputs.append({"output": mock_output})
            eval_scores = evaluate_assertions(mock_output, asserts, {"latency": 50, "cost": 0.001})
            case_cost += 0.001
            for eval_score in eval_scores:
                eval_outputs.append(eval_score)
        return per_trial_outputs, eval_outputs, case_cost

    if is_quick_eval:
        executor = concurrent.futures.ThreadPoolExecutor(max_workers=1)
        for c in cases_data:
            if cost_accumulated >= budget_cost:
                status = "budget_exceeded"
                manifest["status"] = status
                failures.append({"message": f"Budget exceeded at case {c.get('id', 'case-X')}"})
                break

            asserts = c.get('assert', [])

            try:
                if case_timeout is not None:
                    future = executor.submit(execute_case, c, trials, asserts)
                    per_trial_outputs, eval_outputs, case_cost = future.result(timeout=case_timeout)
                else:
                    per_trial_outputs, eval_outputs, case_cost = execute_case(c, trials, asserts)

                cost_accumulated += case_cost
                cases.append({
                    "case_id": c.get('id', 'case-X'),
                    "per_trial_outputs": per_trial_outputs,
                    "evaluator_outputs": eval_outputs,
                    "pointers": {}
                })
            except concurrent.futures.TimeoutError:
                failures.append({"message": f"Timeout exceeded at case {c.get('id', 'case-X')}"})

        executor.shutdown(wait=False)
    else:
        per_trial_outputs = [{"output": f"dummy_{t}"} for t in range(trials)]
        eval_outputs = [{"score": 1.0} for t in range(trials)]
        cases = [
            {
                "case_id": "case-1",
                "per_trial_outputs": per_trial_outputs,
                "evaluator_outputs": eval_outputs,
                "pointers": {}
            }
        ]
    cases_path = os.path.join(output_dir, 'cases.jsonl')
    with open(cases_path, 'w') as f:
        for case in cases:
            f.write(json.dumps(case) + "\n")

    # Write run_manifest.json (updated with status)
    manifest_path = os.path.join(output_dir, 'run_manifest.json')
    with open(manifest_path, 'w') as f:
        json.dump(manifest, f, indent=2)

    # 3. Write failures.json
    failures_path = os.path.join(output_dir, 'failures.json')
    with open(failures_path, 'w') as f:
        json.dump(failures, f, indent=2)

    # 4. Write artifact_refs.json
    artifact_refs = {
        "references": {
            "dummy_ref": {
                "uri": "dummy_uri",
                "digest": "sha256:e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
            }
        }
    }
    artifact_refs_path = os.path.join(output_dir, 'artifact_refs.json')
    with open(artifact_refs_path, 'w') as f:
        json.dump(artifact_refs, f, indent=2)

    # 5. Run scorecard normalizer
    import subprocess
    normalize_script = os.path.join(os.path.dirname(__file__), '../../runs/normalize.py')
    scorecard_path = os.path.join(output_dir, 'scorecard.json')
    subprocess.run([sys.executable, normalize_script, cases_path, scorecard_path], check=True)

    print(f"Artifacts written to {output_dir}")

if __name__ == "__main__":
    main()
