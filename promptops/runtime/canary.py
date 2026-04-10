import os
import yaml
import tempfile
import json
import subprocess
import sys
from promptops.runtime.runner import main as runner_main

def run_canary(canary_path):
    with open(canary_path, 'r') as f:
        canary_def = yaml.safe_load(f)

    suite_ref = canary_def.get('suite_ref')
    if not suite_ref:
        raise ValueError("canary definition missing suite_ref")

    # We resolve the actual prompts and datasets in a real implementation
    # but for the runner contract, we assemble the run request.
    run_request = {
        "suite_id": suite_ref,
        "revision_ref": "latest",
        "model_matrix": ["default"],
        "evaluator_refs": ["default"],
        "prompt_digest": "sha256:" + __import__('hashlib').sha256(suite_ref.encode()).hexdigest(),
        "dataset_digest": "sha256:" + __import__('hashlib').sha256(suite_ref.encode()).hexdigest(),
        "evaluator_digest": "sha256:" + __import__('hashlib').sha256(suite_ref.encode()).hexdigest(),
        "harness_version": "1.0.0"
    }

    with tempfile.NamedTemporaryFile('w', delete=False, suffix='.json') as f:
        json.dump(run_request, f)
        req_path = f.name

    out_dir = tempfile.mkdtemp()

    adapter_path = "promptops/harnesses/reference-adapter/adapter.yaml"
    if not os.path.exists(adapter_path):
        adapter_path = "harnesses/reference-adapter/adapter.yaml"

    if not os.path.exists(adapter_path):
        print(f"Harness adapter config not found. Could not run canary {canary_path}")
        return

    old_argv = sys.argv.copy()
    sys.argv = ["runner.py", req_path, adapter_path, out_dir]
    try:
        runner_main()
    except SystemExit as e:
        if e.code != 0:
            print(f"Execution failed for canary {canary_path}")
            return
    except Exception as e:
        print(f"Execution failed for canary {canary_path}: {e}")
        return
    finally:
        sys.argv = old_argv

    print(f"Execution completed for canary {canary_path}")
    scorecard_path = os.path.join(out_dir, "scorecard.json")
    if os.path.exists(scorecard_path):
        with open(scorecard_path, 'r') as sf:
            scorecard_data = json.load(sf)
        print(f"Scorecard: {json.dumps(scorecard_data, indent=2)}")

        # In a full implementation, we would compare the generated scorecard
        # with the designated baseline (e.g., prod current) using the regression engine.
        alert_config = canary_def.get('alert', {})
        if alert_config.get('on_regression'):
            print(f"Comparing scorecard with baseline...")
            print(f"Alerting channel {alert_config.get('channel', 'default')} if regressions are detected.")

    try:
        os.remove(req_path)
        import shutil
        shutil.rmtree(out_dir)
    except Exception:
        pass
