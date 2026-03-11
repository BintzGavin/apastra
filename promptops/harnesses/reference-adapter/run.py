import sys
import json
import os
from datetime import datetime, timezone

# Import runtime resolver
# Add repo root to path to resolve promptops.runtime
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))
from promptops.runtime.resolve import resolve

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


    run_artifact = {
        "manifest": {
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
        },
        "cases": [
            {
                "case_id": "case-1",
                "per_trial_outputs": [{"output": "dummy"}],
                "evaluator_outputs": [{"score": 1.0}]
            }
        ],
        "failures": failures
    }

    artifact_path = os.path.join(output_dir, 'run_artifact.json')
    with open(artifact_path, 'w') as f:
        json.dump(run_artifact, f, indent=2)

    # Run scorecard normalizer
    import subprocess
    normalize_script = os.path.join(os.path.dirname(__file__), '../../runs/normalize.py')
    subprocess.run([sys.executable, normalize_script, artifact_path], check=True)

    print(f"Artifact written to {artifact_path}")

if __name__ == "__main__":
    main()
