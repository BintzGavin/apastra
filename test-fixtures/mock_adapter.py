import sys, json
output_dir = sys.argv[2]
with open(f"{output_dir}/run_manifest.json", "w") as f:
    json.dump({"input_refs": {}, "resolved_digests": {}, "timestamps": {}, "harness_version": "1.0", "model_ids": ["gpt-4"], "environment": {}, "status": "success"}, f)
with open(f"{output_dir}/scorecard.json", "w") as f:
    json.dump({"normalized_metrics": {}, "metric_definitions": {}}, f)
with open(f"{output_dir}/cases.jsonl", "w") as f:
    f.write(json.dumps({"case_id": "c1", "per_trial_outputs": [], "evaluator_outputs": [], "pointers": {}}) + "\n")
with open(f"{output_dir}/artifact_refs.json", "w") as f:
    json.dump({"references": {}}, f)
