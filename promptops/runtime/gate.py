"""Fail-closed admission of locally trusted run evidence and regression policy.

Content hashes detect alteration; they are not signatures. The caller must obtain
run directories from a trusted producer and explicitly approve its adapter.
"""

from datetime import datetime, timezone
import json
from os.path import relpath
from pathlib import Path
import re

from promptops.runtime.digest import compute_digest_from_dict, compute_digest, load_asset, read_json
from promptops.runtime.evidence import EvidenceError, finite_number, validate_evidence
from promptops.runtime.suite import build_request, validate_asset
from promptops.runtime.adapter_identity import implementation_identity


def admit_run(directory, adapter_path, expected_revision=None, expected_suite=None, check_workspace=False):
    directory = Path(directory)
    if not directory.is_dir() or directory.is_symlink():
        raise EvidenceError("A resolved run directory is required, not an unresolved digest or scorecard")
    for name in ("run_request.json", "evaluation.json", "invocation.json"):
        if not (directory / name).is_file() or (directory / name).is_symlink():
            raise EvidenceError(f"Missing or unsafe admission record: {name}")
    request = read_json(directory / "run_request.json")
    stored_decision = read_json(directory / "evaluation.json")
    if not isinstance(stored_decision, dict) or stored_decision.get("schema_version") != "3.0":
        raise EvidenceError("Legacy evaluation decision: rerun evaluation to produce complete version 3.0 evidence")
    decision = validate_evidence(request, directory)
    invocation = read_json(directory / "invocation.json")
    adapter = load_asset(adapter_path)
    validate_asset(adapter, "harness-adapter")
    if adapter.get("execution_mode") != "measured" or invocation != {
        "adapter_digest": compute_digest(adapter_path), "adapter_id": adapter["id"],
        "adapter_version": adapter.get("version"), "request_digest": decision["request_digest"], "exit_code": 0,
        "implementation_identity": implementation_identity(adapter_path, adapter),
    }:
        raise EvidenceError("Run producer is not the approved measured adapter")
    manifest = read_json(directory / "run_manifest.json")
    if manifest["harness_identifier"] != adapter["id"] or manifest["harness_version"] != adapter.get("version"):
        raise EvidenceError("Run producer identity is inconsistent")
    decision["invocation_digest"] = compute_digest(directory / "invocation.json")
    if stored_decision != decision:
        raise EvidenceError("Stored evaluation decision or content hashes do not match evidence")
    if expected_revision is not None:
        if not re.fullmatch(r"[0-9a-f]{40}", expected_revision) or request.get("source_revision") != expected_revision:
            raise EvidenceError("Run source revision is missing or stale")
    if expected_suite is not None and request["suite_id"] != expected_suite:
        raise EvidenceError("Run belongs to another suite")
    if check_workspace:
        current = build_request(expected_suite or request["suite_id"])
        for field in ("prompt_digest", "dataset_digest", "evaluator_digest", "suite_digest", "model_matrix", "sampling_config", "trials"):
            if current[field] != request[field]:
                raise EvidenceError(f"Run does not describe the tested workspace: {field}")
    return {"request": request, "decision": decision, "manifest": manifest, "scorecard": read_json(directory / "scorecard.json"), "invocation": invocation}


def evaluate_policy(candidate, baseline, policy):
    validate_asset(policy, "regression-policy")
    validate_asset(candidate, "scorecard")
    validate_asset(baseline, "scorecard")
    evidence = []
    failed = False
    warning = False
    seen = set()
    for rule in policy["rules"]:
        metric = rule["metric"]
        if metric in seen:
            raise EvidenceError("Duplicate regression rule")
        seen.add(metric)
        c = candidate["normalized_metrics"].get(metric)
        b = baseline["normalized_metrics"].get(metric)
        definition = candidate["metric_definitions"].get(metric)
        if not finite_number(c) or not finite_number(b) or not definition or definition != baseline["metric_definitions"].get(metric):
            raise EvidenceError(f"Missing measurement or incompatible metric definition: {metric}")
        if definition["direction"] != rule["direction"]:
            raise EvidenceError("Policy direction does not match the metric definition")
        if any(not finite_number(rule[field]) for field in ("floor", "allowed_delta") if field in rule):
            raise EvidenceError("Policy limits must be finite")
        sign = 1 if rule["direction"] == "higher_is_better" else -1
        passed = ("floor" not in rule or sign * c >= sign * rule["floor"])
        if "allowed_delta" in rule:
            passed = passed and sign * c >= sign * b - rule["allowed_delta"]
        evidence.append({"metric": metric, "candidate_value": c, "baseline_value": b, "delta": c - b, "status": "pass" if passed else "fail", "severity": rule["severity"]})
        if not passed:
            failed = failed or rule["severity"] == "blocker"
            warning = warning or rule["severity"] == "warning"
    return {"status": "fail" if failed else "warning" if warning else "pass", "evidence": evidence}


def resolve_baseline(reference, expected_suite):
    path = Path(reference)
    if path.is_dir():
        return path, None
    if path.is_symlink() or not path.is_file() or path.suffix != ".json":
        raise EvidenceError("A baseline record or resolved run directory is required")
    record = read_json(path)
    validate_asset(record, "baseline")
    if record["suite_id"] != expected_suite:
        raise EvidenceError("Baseline record belongs to another suite")
    directory = Path(record["run_path"])
    if not directory.is_absolute():
        directory = path.parent / directory
    return directory, record


def regression(candidate_dir, baseline_dir, policy_path, adapter_path, expected_revision=None, expected_suite=None, check_workspace=False):
    candidate = admit_run(candidate_dir, adapter_path, expected_revision, expected_suite, check_workspace)
    baseline_dir, record = resolve_baseline(baseline_dir, candidate["request"]["suite_id"])
    baseline = admit_run(baseline_dir, adapter_path, expected_suite=candidate["request"]["suite_id"])
    if record is not None and record["run_digest"] != compute_digest(Path(baseline_dir) / "evaluation.json"):
        raise EvidenceError("Baseline record run digest does not match its evidence")
    if candidate["invocation"]["implementation_identity"] != baseline["invocation"]["implementation_identity"]:
        raise EvidenceError("Incompatible adapter implementation identities")
    if baseline["decision"]["status"] != "pass":
        raise EvidenceError("Baseline is not an eligible passing evaluation")
    for field in ("suite_id", "dataset_digest", "evaluator_digest", "required_metrics", "model_matrix", "sampling_config", "trials", "harness_version", "expected_case_ids", "thresholds", "budgets", "timeouts"):
        if candidate["request"][field] != baseline["request"][field]:
            raise EvidenceError(f"Incompatible regression inputs: {field}")
    for field in set(candidate["request"]["suite"]) | set(baseline["request"]["suite"]):
        if field not in {"prompt", "name", "description"} and candidate["request"]["suite"].get(field) != baseline["request"]["suite"].get(field):
            raise EvidenceError(f"Incompatible regression suite configuration: {field}")
    policy = policy_path if isinstance(policy_path, dict) else load_asset(policy_path)
    # Pooled evidence remains descriptive; each requested model must satisfy policy.
    report = evaluate_policy(candidate["scorecard"], baseline["scorecard"], policy)
    model_results = {}
    for model in candidate["request"]["model_matrix"]:
        candidate_card = {**candidate["scorecard"], "normalized_metrics": candidate["decision"]["model_results"][model]["metrics"]}
        baseline_card = {**baseline["scorecard"], "normalized_metrics": baseline["decision"]["model_results"][model]["metrics"]}
        model_results[model] = evaluate_policy(candidate_card, baseline_card, policy)
    statuses = {result["status"] for result in model_results.values()}
    report.update({
        "schema_version": "3.0", "model_results": model_results,
        "status": "fail" if "fail" in statuses else "warning" if "warning" in statuses else "pass",
    })
    if candidate["decision"]["status"] != "pass":
        report["status"] = "fail"
    c_cost, b_cost = candidate["manifest"].get("total_cost"), baseline["manifest"].get("total_cost")
    if c_cost is not None and b_cost is not None:
        report["cost_delta"] = c_cost - b_cost
    report.update({
        "candidate_ref": compute_digest(Path(candidate_dir) / "evaluation.json"),
        "baseline_ref": compute_digest(Path(baseline_dir) / "evaluation.json"),
        "policy_digest": compute_digest_from_dict(policy), "source_revision": candidate["request"].get("source_revision"),
        "suite_id": candidate["request"]["suite_id"],
    })
    validate_asset(report, "regression-report")
    return report


def establish_baseline(suite_id, name, directory, adapter_path):
    if not all(isinstance(value, str) and re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9._-]*", value) for value in (suite_id, name)):
        raise EvidenceError("Baseline suite and name must be safe identifiers")
    run = admit_run(directory, adapter_path, expected_suite=suite_id)
    if run["decision"]["status"] != "pass":
        raise EvidenceError("Only an eligible passing run can establish a baseline")
    path = Path("derived-index/baselines") / f"{suite_id}-{name}.json"
    record = {
        "baseline_id": f"{suite_id}-{name}", "suite_id": suite_id,
        "run_digest": compute_digest(Path(directory) / "evaluation.json"),
        "run_path": relpath(Path(directory).resolve(), path.parent.resolve()),
        "created_at": datetime.now(timezone.utc).isoformat(),
    }
    validate_asset(record, "baseline")
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("x", encoding="utf-8") as handle:
        json.dump(record, handle, indent=2, allow_nan=False)
        handle.write("\n")
    return {"status": "pass", "baseline_path": str(path), **record}
