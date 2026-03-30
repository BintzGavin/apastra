import sys
import json
import subprocess
import os
import uuid
import shutil

def handle_request(request_line):
    try:
        req = json.loads(request_line)
    except json.JSONDecodeError:
        return None

    req_id = req.get("id")
    method = req.get("method")

    if method == "tools/list":
        tool_def = {
            "name": "run_eval",
            "description": "Executes an evaluation suite against a prompt and dataset, returning a scorecard summary.",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "suite_id": { "type": "string" },
                    "revision_ref": { "type": "string" },
                    "model_matrix": { "type": "array", "items": { "type": "string" } },
                    "evaluator_refs": { "type": "array", "items": { "type": "string" } },
                    "prompt_digest": { "type": "string" },
                    "dataset_digest": { "type": "string" },
                    "evaluator_digest": { "type": "string" },
                    "harness_version": { "type": "string" }
                },
                "required": ["suite_id", "revision_ref", "model_matrix", "evaluator_refs", "prompt_digest", "dataset_digest", "evaluator_digest", "harness_version"]
            },
            "type": "function"
        }
        return {
            "jsonrpc": "2.0",
            "id": req_id,
            "result": {
                "tools": [tool_def]
            }
        }
    elif method == "tools/call":
        params = req.get("params", {})
        name = params.get("name")
        args = params.get("arguments", {})

        if name == "run_eval":
            run_id = str(uuid.uuid4())
            run_dir = f"promptops/runs/{run_id}"
            os.makedirs(run_dir, exist_ok=True)

            run_request_path = os.path.join(run_dir, "run_request.json")
            with open(run_request_path, "w") as f:
                json.dump(args, f)

            adapter_yaml = "promptops/harnesses/reference-adapter/adapter.yaml"
            if not os.path.exists(adapter_yaml):
                return {
                    "jsonrpc": "2.0",
                    "id": req_id,
                    "error": {
                        "code": -32603,
                        "message": "Reference adapter not found."
                    }
                }

            cmd = ["bash", "promptops/runs/runner-shim.sh", adapter_yaml, run_request_path, run_dir]
            try:
                result = subprocess.run(cmd, check=True, capture_output=True, text=True)

                scorecard_path = os.path.join(run_dir, "scorecard.json")
                if os.path.exists(scorecard_path):
                    with open(scorecard_path, "r") as f:
                        scorecard = json.load(f)

                    return {
                        "jsonrpc": "2.0",
                        "id": req_id,
                        "result": {
                            "content": [
                                {
                                    "type": "text",
                                    "text": json.dumps(scorecard, indent=2)
                                }
                            ]
                        }
                    }
                else:
                    return {
                        "jsonrpc": "2.0",
                        "id": req_id,
                        "error": {
                            "code": -32603,
                            "message": "Scorecard not generated."
                        }
                    }
            except subprocess.CalledProcessError as e:
                return {
                    "jsonrpc": "2.0",
                    "id": req_id,
                    "error": {
                        "code": -32603,
                        "message": f"Execution failed: {e.stderr}"
                    }
                }
        else:
            return {
                "jsonrpc": "2.0",
                "id": req_id,
                "error": {
                    "code": -32601,
                    "message": "Tool not found"
                }
            }

    return {
        "jsonrpc": "2.0",
        "id": req_id,
        "error": {
            "code": -32601,
            "message": "Method not found"
        }
    }

def main():
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue

        resp = handle_request(line)
        if resp:
            print(json.dumps(resp))
            sys.stdout.flush()

if __name__ == "__main__":
    main()
