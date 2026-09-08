"""Measured local program demo. No model, network, credentials, or canned scores."""
from datetime import datetime, timezone
import json
from pathlib import Path
import sys


def main():
    request_path, output_path = map(Path, sys.argv[1:])
    request = json.loads(request_path.read_text())
    started = datetime.now(timezone.utc).isoformat()
    operations = {"Uppercase {{text}}": str.upper, "Lowercase {{text}}": str.lower}
    operation = operations[request["prompt"]["template"]]
    if request["model_matrix"] != ["local:text-assistant"] or set(request["required_metrics"]) != {"exact_match_score"}:
        raise ValueError("This local demo supports only the text assistant and exact-match evaluator")
    cases, scores = [], []
    for source in request["cases"]:
        trials = []
        for trial_id in range(1, request["trials"] + 1):
            output = operation(source["inputs"]["text"])
            score = float(output == source["expected_outputs"]["text"])
            scores.append(score)
            trials.append({"trial_id": trial_id, "output": output, "evaluator_outputs": {"exact_match_score": score}})
        cases.append({"case_id": source["case_id"], "model_id": "local:text-assistant", "per_trial_outputs": trials})
    manifest = {
        "input_refs": {}, "resolved_digests": {name: request[name] for name in ("prompt_digest", "suite_digest", "dataset_digest", "evaluator_digest")},
        "timestamps": {"started_at": started, "completed_at": datetime.now(timezone.utc).isoformat()},
        "harness_identifier": "local-text-assistant", "harness_version": "1.0.0", "model_ids": request["model_matrix"],
        "sampling_config": request["sampling_config"], "environment": {}, "execution_mode": "measured", "status": "completed", "total_cost": 0,
    }
    for name, data in {
        "run_manifest.json": manifest,
        "scorecard.json": {"normalized_metrics": {"exact_match_score": sum(scores) / len(scores)}, "metric_definitions": request["required_metrics"]},
        "artifact_refs.json": {"references": {}},
    }.items():
        (output_path / name).write_text(json.dumps(data) + "\n")
    (output_path / "cases.jsonl").write_text("".join(json.dumps(case) + "\n" for case in cases))


if __name__ == "__main__":
    main()
