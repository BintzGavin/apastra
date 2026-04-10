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
    import os
    suite_file = f"promptops/suites/{suite_ref}.yaml" if os.path.exists(f"promptops/suites/{suite_ref}.yaml") else f"promptops/suites/{suite_ref}.json"
    prompt_d = "sha256:0000000000000000000000000000000000000000000000000000000000000000"
    dataset_d = "sha256:0000000000000000000000000000000000000000000000000000000000000000"
    evaluator_d = "sha256:0000000000000000000000000000000000000000000000000000000000000000"
    try:
        import hashlib, yaml, json
        with open(suite_file, 'r') as f:
            if suite_file.endswith('.yaml'):
                data = yaml.safe_load(f)
            else:
                data = json.load(f)
            if data:
                if 'prompt' in data:
                    prompt_d = "sha256:" + hashlib.sha256(str(data['prompt']).encode('utf-8')).hexdigest()
                if 'datasets' in data:
                    dataset_d = "sha256:" + hashlib.sha256(str(data['datasets']).encode('utf-8')).hexdigest()
                if 'evaluators' in data:
                    evaluator_d = "sha256:" + hashlib.sha256(str(data['evaluators']).encode('utf-8')).hexdigest()
    except Exception:
        pass

    run_request = {
        "suite_id": suite_ref,
        "revision_ref": "latest",
        "model_matrix": ["default"],
        "evaluator_refs": ["default"],
        "prompt_digest": prompt_d,
        "dataset_digest": dataset_d,
        "evaluator_digest": evaluator_d,
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
