"""Admission checks shared by evaluation, comparison, and quality gates."""

import json
import hashlib
import math
from pathlib import Path

from promptops.runtime.digest import compute_digest, compute_digest_from_dict, dataset_digest, group_digest, parse_json, read_json


class EvidenceError(ValueError):
    pass


def finite_number(value):
    return type(value) in (int, float) and math.isfinite(value)


def validate_request(request):
    from promptops.runtime.suite import validate_asset
    validate_asset(request, "run-request")
    validate_asset(request["suite"], "suite")
    validate_asset(request["prompt"], "prompt-spec")
    expected = {
        "prompt_digest": compute_digest_from_dict(request["prompt"]),
        "suite_digest": compute_digest_from_dict(request["suite"]),
        "dataset_digest": group_digest("datasets", [dataset_digest(rows) for rows in request["datasets"]]),
        "evaluator_digest": group_digest("evaluators", [compute_digest_from_dict(item) for item in request["evaluators"]]),
    }
    if any(request[key] != digest for key, digest in expected.items()):
        raise EvidenceError("Request digest does not match its input snapshot")
    if request["cases"] != [case for rows in request["datasets"] for case in rows]:
        raise EvidenceError("Dataset snapshot does not match requested cases")
    for case in request["cases"]:
        validate_asset(case, "dataset-case")
    if request["expected_case_ids"] != [case["case_id"] for case in request["cases"]]:
        raise EvidenceError("Expected case IDs do not match the dataset snapshot")
    metrics = {}
    for evaluator in request["evaluators"]:
        validate_asset(evaluator, "evaluator")
        if set(evaluator["metrics"]) != set(evaluator["metric_definitions"]) or set(metrics) & set(evaluator["metrics"]):
            raise EvidenceError("Evaluator metric coverage is inconsistent")
        metrics.update(evaluator["metric_definitions"])
    if request["required_metrics"] != metrics:
        raise EvidenceError("Required metrics do not match evaluator definitions")
    suite = request["suite"]
    if request["suite_id"] != suite["id"] or request["evaluator_refs"] != suite["evaluators"]:
        raise EvidenceError("Suite identity does not match the snapshot")
    for key, default in (("thresholds", {}), ("budgets", {}), ("timeouts", {}), ("trials", 1), ("sampling_config", {})):
        if request.get(key, default) != suite.get(key, default):
            raise EvidenceError(f"Request overrides declared suite policy: {key}")
    if set(request.get("thresholds", {})) - set(metrics):
        raise EvidenceError("Suite thresholds reference undefined metrics")


def validate_evidence(request, directory):
    validate_request(request)
    directory = Path(directory)
    names = ("run_manifest.json", "scorecard.json", "cases.jsonl", "artifact_refs.json")
    for name in names:
        path = directory / name
        if not path.is_file() or path.is_symlink():
            raise EvidenceError(f"Missing or unsafe evidence file: {name}")
    manifest = read_json(directory / "run_manifest.json")
    scorecard = read_json(directory / "scorecard.json")
    from promptops.runtime.suite import validate_asset
    validate_asset(manifest, "run-manifest")
    validate_asset(scorecard, "scorecard")
    references = read_json(directory / "artifact_refs.json")
    validate_asset(references, "artifact-refs")
    from promptops.runtime.suite import safe_reference
    for reference in references["references"].values():
        uri = reference["uri"]
        safe_reference(uri)
        path = directory / uri
        if ":" in uri or not path.resolve().is_relative_to(directory.resolve()) or path.is_symlink() or not path.is_file():
            raise EvidenceError("Artifact reference must resolve to a retained local file")
        actual = "sha256:" + hashlib.sha256(path.read_bytes()).hexdigest()
        if reference["digest"] != actual:
            raise EvidenceError("Artifact reference content digest mismatch")
    if manifest.get("execution_mode") != "measured":
        raise EvidenceError("Only measured execution is eligible for evaluation")
    if manifest.get("status") != "completed":
        raise EvidenceError("Harness execution did not complete")
    if manifest["harness_version"] != request["harness_version"] or manifest["sampling_config"] != request.get("sampling_config", {}):
        raise EvidenceError("Harness version or sampling configuration mismatch")
    models = request.get("model_matrix", [])
    if not models or len(set(models)) != len(models) or manifest.get("model_ids") != models:
        raise EvidenceError("Run model identity does not match the request")
    for name in ("prompt_digest", "dataset_digest", "evaluator_digest", "suite_digest"):
        if not request.get(name) or manifest.get("resolved_digests", {}).get(name) != request[name]:
            raise EvidenceError(f"Resolved identity mismatch: {name}")
    required = request.get("required_metrics", {})
    metrics = scorecard.get("normalized_metrics", {})
    definitions = scorecard.get("metric_definitions", {})
    if not required or set(metrics) != set(required) or set(definitions) != set(required):
        raise EvidenceError("Missing or unexpected evaluation metrics/definitions")
    for name, value in metrics.items():
        if not finite_number(value):
            raise EvidenceError(f"Invalid metric value: {name}")
        for field in ("version", "direction", "unit"):
            if not required[name].get(field) or definitions[name].get(field) != required[name][field]:
                raise EvidenceError(f"Metric definition mismatch: {name}.{field}")
    expected_cases = request.get("expected_case_ids", [])
    trials = request.get("trials", 1)
    if not expected_cases or len(set(expected_cases)) != len(expected_cases) or type(trials) is not int or trials < 1:
        raise EvidenceError("A nonempty case set and positive trial count are required")
    expected = {(model, case) for model in models for case in expected_cases}
    seen = set()
    values = {name: [] for name in required}
    with (directory / "cases.jsonl").open(encoding="utf-8") as handle:
        for line in handle:
            if not line.strip():
                continue
            case = parse_json(line)
            validate_asset(case, "run-case")
            key = (case.get("model_id"), case.get("case_id"))
            if key not in expected or key in seen:
                raise EvidenceError("Unexpected or duplicate case/model result")
            seen.add(key)
            outputs = case.get("per_trial_outputs", [])
            if len(outputs) != trials or {item.get("trial_id") for item in outputs} != set(range(1, trials + 1)):
                raise EvidenceError("Missing or duplicate trial result")
            for output in outputs:
                scores = output.get("evaluator_outputs", {})
                if "output" not in output or set(scores) != set(required):
                    raise EvidenceError("Incomplete trial output or evaluator coverage")
                for name, value in scores.items():
                    if not finite_number(value):
                        raise EvidenceError(f"Invalid trial metric: {name}")
                    values[name].append(value)
    if seen != expected:
        raise EvidenceError("Incomplete case/model coverage")
    for name, measured in values.items():
        mean = math.fsum(measured) / len(measured)
        if not math.isclose(mean, metrics[name], rel_tol=1e-12, abs_tol=1e-12):
            raise EvidenceError(f"Scorecard does not match case evidence: {name}")
    thresholds = request.get("thresholds", {})
    failures = []
    for name, threshold in thresholds.items():
        if name not in metrics or not finite_number(threshold):
            raise EvidenceError(f"Invalid or missing threshold metric: {name}")
        direction = required[name]["direction"]
        if direction not in ("higher_is_better", "lower_is_better"):
            raise EvidenceError(f"Unknown metric direction: {name}")
        if (direction == "higher_is_better" and metrics[name] < threshold) or (direction == "lower_is_better" and metrics[name] > threshold):
            failures.append(name)
    budget = request.get("budgets", {}).get("cost_budget")
    if budget is not None:
        cost = manifest.get("total_cost")
        if not finite_number(budget) or budget < 0 or not finite_number(cost) or cost < 0:
            raise EvidenceError("Cost budget requires valid measured cost")
        if cost > budget:
            failures.append("cost_budget")
    return {
        "status": "fail" if failures else "pass" if thresholds else "not_evaluated",
        "execution_status": "completed", "suite_id": request["suite_id"],
        "metrics": metrics, "failed_criteria": failures,
        "artifact_digests": {name: compute_digest(str(directory / name)) for name in names},
        "request_digest": compute_digest(str(directory / "run_request.json")),
    }
