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

    cases_data = []
    if is_quick_eval and dataset_path and os.path.exists(dataset_path):
        with open(dataset_path, 'r') as df:
            for line in df:
                if line.strip():
                    cases_data.append(json.loads(line))

    # 1. Write run_manifest.json
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
        "status": status
    }
    manifest_path = os.path.join(output_dir, 'run_manifest.json')
    with open(manifest_path, 'w') as f:
        json.dump(manifest, f, indent=2)

    # 2. Write cases.jsonl
    cases = []
    if is_quick_eval:
        for c in cases_data:
            eval_outputs = []
            asserts = c.get('assert', [])
            # Using real evaluation logic
            mock_output = "mock_output"
            eval_scores = evaluate_assertions(mock_output, asserts)
            # evaluate_assertions returns a list of dictionaries [{"assert_<type>": score}, ...]
            for eval_score in eval_scores:
                eval_outputs.append(eval_score)

            cases.append({
                "case_id": c.get('id', 'case-X'),
                "per_trial_outputs": [{"output": mock_output}],
                "evaluator_outputs": eval_outputs,
                "pointers": {}
            })
    else:
        cases = [
            {
                "case_id": "case-1",
                "per_trial_outputs": [{"output": "dummy"}],
                "evaluator_outputs": [{"score": 1.0}],
                "pointers": {}
            }
        ]
    cases_path = os.path.join(output_dir, 'cases.jsonl')
    with open(cases_path, 'w') as f:
        for case in cases:
            f.write(json.dumps(case) + "\n")

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
