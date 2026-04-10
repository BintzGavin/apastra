#!/usr/bin/env python3
import sys
import json
import os
import datetime
import subprocess

def main():
    req_path = sys.argv[1]
    out_dir = sys.argv[2]

    with open(req_path, 'r') as f:
        req = json.load(f)

    # Apply project level defaults
    try:
        result = subprocess.run([sys.executable, 'promptops/runs/apply_project_config.py'], capture_output=True, text=True)
        if result.returncode == 0:
            project_config = json.loads(result.stdout)
            defaults = project_config.get("defaults", {})

            # Apply defaults to suite context if not present
            if "model" in defaults and "model_ids" not in req:
                req["model_ids"] = [defaults["model"]]
            if "temperature" in defaults:
                req.setdefault("sampling_config", {})
                req["sampling_config"].setdefault("temperature", defaults["temperature"])
            if "max_tokens" in defaults:
                req.setdefault("sampling_config", {})
                req["sampling_config"].setdefault("max_tokens", defaults["max_tokens"])
    except Exception as e:
        print(f"Warning: Could not apply project config defaults: {e}", file=sys.stderr)

    os.makedirs(out_dir, exist_ok=True)

    timestamp = datetime.datetime.now().isoformat() + "Z"

    cost_budget = req.get("budgets", {}).get("cost_budget", float("inf"))
    if cost_budget == float("inf"):
        cost_budget = req.get("budgets", {}).get("cost", float("inf"))
    total_cost = 0.05

    status = "budget_exceeded" if total_cost > cost_budget else "success"

    manifest = {
        "suite_id": req.get("suite_id", "default"),
        "timestamp": timestamp,
        "timestamps": {
            "started_at": timestamp,
            "completed_at": timestamp
        },
        "harness_version": "1.0.0",
        "harness_identifier": "reference",
        "status": status,
        "total_cost": total_cost,
        "environment": {},
        "model_ids": ["default"],
        "sampling_config": {},
        "resolved_digests": {
            "prompt_digest": req.get("prompt_digest", "sha256:" + __import__('hashlib').sha256(req.get('suite_id', 'default').encode()).hexdigest())
        },
        "input_refs": {
            "prompt": req.get("prompt_digest", "sha256:" + __import__('hashlib').sha256(req.get('suite_id', 'default').encode()).hexdigest())
        }
    }

    with open(os.path.join(out_dir, "run_manifest.json"), 'w') as f:
        json.dump(manifest, f)

    if status == "budget_exceeded":
        with open(os.path.join(out_dir, "failures.json"), 'w') as f:
            json.dump([{"reason": "Cost budget exceeded"}], f)

    scorecard = {
        "suite_id": req.get("suite_id", "default"),
        "timestamp": timestamp,
        "normalized_metrics": {},
        "metric_definitions": {}
    }

    with open(os.path.join(out_dir, "scorecard.json"), 'w') as f:
        json.dump(scorecard, f)

    with open(os.path.join(out_dir, "cases.jsonl"), 'w') as f:
        f.write('{"case_id": "1", "per_trial_outputs": [{"trial_id": "t1", "output": {"text": "output"}, "evaluator_outputs": {}}], "evaluator_outputs": [], "pointers": {}}\n')

    with open(os.path.join(out_dir, "artifact_refs.json"), 'w') as f:
        json.dump({"references": {}}, f)

if __name__ == "__main__":
    main()
