"""Compile an inline quick eval into the same measured execution contract."""

from pathlib import Path
import re
import subprocess
import uuid

from promptops.runtime.digest import compute_digest_from_dict, dataset_digest, load_asset
from promptops.runtime.evidence import EvidenceError, validate_request
from promptops.runtime.suite import validate_asset


def build_quick_request(path, models, harness_version="1.0.0"):
    data = load_asset(path)
    validate_asset(data, "quick-eval")
    if not models:
        raise EvidenceError("Quick eval requires explicit --models and a measured adapter")
    cases = data["cases"]
    variables = set(re.findall(r"{{\s*([A-Za-z_][A-Za-z_0-9]*)\s*}}", data["prompt"]))
    for case in cases:
        if set(case["inputs"]) != variables or not case.get("assert"):
            raise EvidenceError("Every quick-eval case must supply prompt variables and nonempty assertions")
    prompt = {"id": data["id"] + "-prompt", "template": data["prompt"], "variables": {name: {} for name in sorted(variables)}}
    definitions = {"pass_rate": {"version": "1.0.0", "direction": "higher_is_better", "unit": "ratio"}}
    evaluator = {"id": "inline-assertions-v2", "type": "deterministic", "metrics": ["pass_rate"], "metric_definitions": definitions, "config": {"source": "case.assert", "aggregation": "all assertions pass per trial; mean across trials"}}
    suite = {"id": data["id"], "name": data["id"], "prompt": prompt["id"], "datasets": [data["id"] + "-cases"], "evaluators": [evaluator["id"]], "model_matrix": models, "trials": 1, "thresholds": data.get("thresholds", {}), "extensions": {"quick_eval_digest": compute_digest_from_dict(data)}}
    revision = subprocess.run(["git", "rev-parse", "HEAD"], capture_output=True, text=True)
    request = {
        "suite_id": suite["id"], "revision_ref": "workspace", "requested_revision": "workspace", "source_revision": revision.stdout.strip() if revision.returncode == 0 else None,
        "model_matrix": models, "evaluator_refs": suite["evaluators"], "harness_version": harness_version,
        "prompt_digest": compute_digest_from_dict(prompt), "dataset_digest": dataset_digest(cases), "evaluator_digest": compute_digest_from_dict(evaluator), "suite_digest": compute_digest_from_dict(suite),
        "prompt": prompt, "cases": cases, "datasets": [cases], "evaluators": [evaluator], "suite": suite,
        "expected_case_ids": [case["case_id"] for case in cases], "required_metrics": definitions,
        "trials": 1, "thresholds": suite["thresholds"], "budgets": {}, "timeouts": {}, "sampling_config": {},
    }
    validate_request(request)
    return request


def evaluate_quick(path, models, adapter, output_dir=None):
    from promptops.runtime.runner import run
    request = build_quick_request(path, models, harness_version=load_asset(adapter).get("version"))
    output = Path(output_dir or Path("promptops/runs") / f"quick-{uuid.uuid4().hex}").resolve()
    return {**run(request, adapter, output), "output_dir": str(output)}
