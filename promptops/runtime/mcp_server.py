import os
import json
import glob
import subprocess
import tempfile
import yaml
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("promptops")

@mcp.tool()
def list_suites() -> list:
    """Lists available evaluation suites in the current workspace."""
    suites = []
    suite_files = glob.glob('promptops/suites/*.yaml') + glob.glob('promptops/suites/*.json')
    if not suite_files:
        suite_files = glob.glob('suites/*.yaml') + glob.glob('suites/*.json')
    for suite_file in suite_files:
        try:
            with open(suite_file, 'r') as f:
                if suite_file.endswith('.yaml'):
                    data = yaml.safe_load(f)
                else:
                    data = json.load(f)
                if data and "id" in data:
                    suites.append({
                        "id": data["id"],
                        "name": data.get("name", ""),
                        "description": data.get("description", "")
                    })
        except Exception:
            pass
    return suites

@mcp.tool()
def run_evaluation(suite_id: str, revision_ref: str = "latest") -> str:
    """Runs a PromptOps evaluation suite.

    Args:
        suite_id: The ID of the evaluation suite to run.
        revision_ref: The reference to test against (e.g. latest, commit sha).
    """
    import os
    suite_file = f"promptops/suites/{suite_id}.yaml" if os.path.exists(f"promptops/suites/{suite_id}.yaml") else f"promptops/suites/{suite_id}.json"
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
        "suite_id": suite_id,
        "revision_ref": revision_ref,
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
        return json.dumps({
            "status": "error",
            "message": f"Harness adapter config not found. Could not run suite {suite_id}",
            "suite_id": suite_id
        })

    current_dir = os.path.dirname(os.path.abspath(__file__))
    runner_path = os.path.join(current_dir, "runner.py")

    cmd = ["python", runner_path, req_path, adapter_path, out_dir]
    result = subprocess.run(cmd, capture_output=True, text=True)

    if result.returncode != 0:
        try:
            os.remove(req_path)
            import shutil
            shutil.rmtree(out_dir)
        except Exception:
            pass

        return json.dumps({
            "status": "error",
            "message": f"Execution failed for suite {suite_id}",
            "error": result.stderr or result.stdout
        })

    try:
        scorecard_path = os.path.join(out_dir, "scorecard.json")
        scorecard_data = None
        if os.path.exists(scorecard_path):
            with open(scorecard_path, 'r') as sf:
                scorecard_data = json.load(sf)

        try:
            os.remove(req_path)
            import shutil
            shutil.rmtree(out_dir)
        except Exception:
            pass

        if scorecard_data:
            return json.dumps({
                "status": "success",
                "message": f"Execution completed for suite {suite_id}",
                "scorecard": scorecard_data
            })
    except Exception as e:
        try:
            os.remove(req_path)
            import shutil
            shutil.rmtree(out_dir)
        except Exception:
            pass

    return json.dumps({
        "status": "success",
        "message": f"Execution completed for suite {suite_id}, but scorecard not found"
    })

def start_mcp_server():
    mcp.run()
