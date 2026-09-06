"""Deterministic process target for acceptance tests, not an LLM benchmark.

Only uppercase/lowercase text and exact equality assertions are supported.
Every score below is calculated from the declared input and actual output.
"""

import json
import hashlib
from datetime import datetime, timezone
from pathlib import Path
import sys
import time


variant, request_path, output_path = sys.argv[1:]
started = datetime.now(timezone.utc).isoformat()
request = json.loads(Path(request_path).read_text())
destination = Path(output_path)
destination.mkdir(parents=True, exist_ok=True)
if variant == "process-failure" or "local:broken" in request["model_matrix"]:
    raise SystemExit(7)
if variant == "timeout":
    time.sleep(1)
if request["prompt"]["template"] != "Uppercase {{text}}":
    raise SystemExit("Unsupported deterministic target prompt")
definitions = request["required_metrics"]
if set(definitions) not in ({"exact_match_score"}, {"pass_rate"}):
    raise SystemExit("Unsupported deterministic target evaluator")
cases = []
values = []
for model in request["model_matrix"]:
    if model not in ("local:uppercase", "local:lowercase"):
        raise SystemExit("Unsupported deterministic target model")
    for source in request["cases"]:
        outputs = []
        for trial in range(1, request["trials"] + 1):
            output = source["inputs"]["text"].upper() if model == "local:uppercase" else source["inputs"]["text"].lower()
            if "pass_rate" in definitions:
                assertions = source["assert"]
                if not assertions or any(row["type"] != "equals" for row in assertions):
                    raise SystemExit("Only exact equality assertions are supported by this test target")
                score = float(all(output == row["value"] for row in assertions))
            else:
                score = float(output == source["expected_outputs"]["text"])
            metrics = {next(iter(definitions)): score}
            outputs.append({"trial_id": trial, "output": output, "evaluator_outputs": metrics})
            values.append(score)
        cases.append({"case_id": source["case_id"], "model_id": model, "per_trial_outputs": outputs})
metrics = {next(iter(definitions)): sum(values) / len(values)}
manifest = {
    "input_refs": {},
    "resolved_digests": {key: request[key] for key in ("prompt_digest", "dataset_digest", "evaluator_digest", "suite_digest")},
    "timestamps": {"started_at": started, "completed_at": datetime.now(timezone.utc).isoformat()},
    "harness_identifier": "deterministic-test-target",
    "harness_version": "1.0.0", "model_ids": request["model_matrix"],
    "sampling_config": request.get("sampling_config", {}), "environment": {},
    "execution_mode": "measured", "status": "completed",
}
if variant == "empty-metrics":
    metrics = {}
elif variant == "empty-cases":
    cases = []
elif variant == "wrong-model":
    manifest["model_ids"] = ["never-requested"]
elif variant == "failed-manifest":
    manifest["status"] = "failed"
elif variant == "fixture":
    manifest["execution_mode"] = "fixture"
elif variant == "wrong-digest":
    manifest["resolved_digests"]["prompt_digest"] = "sha256:" + "0" * 64
elif variant == "duplicate-case":
    cases.append(cases[0])
elif variant == "duplicate-trial":
    cases[0]["per_trial_outputs"].append(cases[0]["per_trial_outputs"][0])
elif variant == "score-drift":
    metrics[next(iter(definitions))] = 0.25
elif variant == "request-tamper":
    changed = dict(request)
    changed["source_revision"] = "b" * 40
    Path(request_path).write_text(json.dumps(changed))
elif variant == "zero-cost":
    manifest["total_cost"] = 0
elif variant == "invalid-cost":
    manifest["total_cost"] = -1

references = {}
if variant == "raw-reference":
    trace = b"local deterministic trace\n"
    (destination / "trace.txt").write_bytes(trace)
    references["trace"] = {"uri": "trace.txt", "digest": "sha256:" + hashlib.sha256(trace).hexdigest()}

for name, payload in {
    "run_manifest.json": manifest,
    "scorecard.json": {"normalized_metrics": metrics, "metric_definitions": definitions},
    "artifact_refs.json": {"references": references},
}.items():
    (destination / name).write_text(json.dumps(payload))
(destination / "cases.jsonl").write_text("".join(json.dumps(case) + "\n" for case in cases))
