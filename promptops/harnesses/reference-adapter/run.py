#!/usr/bin/env python3
import sys
import json
import os
import datetime

def main():
    req_path = sys.argv[1]
    out_dir = sys.argv[2]

    with open(req_path, 'r') as f:
        req = json.load(f)

    os.makedirs(out_dir, exist_ok=True)

    timestamp = datetime.datetime.now().isoformat() + "Z"

    cost_budget = req.get("budgets", {}).get("cost", float("inf"))
    total_cost = 0.05

    manifest = {
        "suite_id": req.get("suite_id", "default"),
        "timestamp": timestamp,
        "timestamps": {
            "started_at": timestamp,
            "completed_at": timestamp
        },
        "harness_version": "1.0.0",
        "harness_identifier": "reference",
        "status": "budget_exceeded" if total_cost > cost_budget else "success",
        "total_cost": total_cost,
        "environment": {},
        "model_ids": ["default"],
        "sampling_config": {},
        "resolved_digests": {
            "prompt_digest": "sha256:0000000000000000000000000000000000000000000000000000000000000000"
        },
        "input_refs": {
            "prompt": req.get("prompt_digest", "sha256:0000000000000000000000000000000000000000000000000000000000000000")
        }
    }

    with open(os.path.join(out_dir, "run_manifest.json"), 'w') as f:
        json.dump(manifest, f)

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
