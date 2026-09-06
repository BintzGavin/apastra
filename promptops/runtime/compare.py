"""Compare complete measured runs while retaining their evidence."""

from copy import deepcopy
from pathlib import Path
import math
import time
import uuid

from promptops.runtime.evidence import EvidenceError, finite_number
from promptops.runtime.digest import load_asset
from promptops.runtime.runner import run
from promptops.runtime.suite import build_request, validate_asset


def invoke_harness(run_request, adapter_config=None, out_dir=None, execution_timeout=None):
    if not adapter_config:
        raise ValueError("An evaluation adapter is required")
    result = run(run_request, adapter_config, out_dir, execution_timeout=execution_timeout)
    if result["status"] != "pass":
        raise EvidenceError(f"Harness evaluation did not pass: {result['status']}")
    return result


def aggregate_scorecards(suite_id, individual_scorecards):
    if not individual_scorecards:
        raise EvidenceError("A comparison requires measured results")
    metrics = {}
    tradeoffs = {"cost": {}, "quality": {}, "latency": {}}
    for model, card in individual_scorecards.items():
        values = card.get("normalized_metrics", {})
        if not values or any(not finite_number(value) for value in values.values()):
            raise EvidenceError("Comparison metrics must be nonempty finite measurements")
        metrics[model] = values
        for metric, axis in (("cost_usd", "cost"), ("exact_match_score", "quality"), ("latency_ms", "latency")):
            if metric in values:
                tradeoffs[axis][model] = values[metric]
    if len({tuple(sorted(values)) for values in metrics.values()}) != 1:
        raise EvidenceError("Compared runs must have the same metric set")
    return {"suite_id": suite_id, "models": list(metrics), "metrics": metrics, "comparison_tradeoffs": tradeoffs}


def run_comparison(suite_id, models=None, adapter_config=None, output_dir=None):
    if not adapter_config:
        raise ValueError("An evaluation adapter is required")
    request = build_request(suite_id, models, harness_version=load_asset(adapter_config).get("version"))
    directory = Path(output_dir or Path("promptops/runs") / f"comparison-{uuid.uuid4().hex}").resolve()
    directory.mkdir(parents=True, exist_ok=True)
    if any(directory.iterdir()):
        raise EvidenceError("Comparison output directory must be empty")
    scorecards, runs = {}, {}
    costs = {}
    started = time.monotonic()
    time_budget = request.get("budgets", {}).get("time")
    cost_budget = request.get("budgets", {}).get("cost_budget")
    for index, model in enumerate(request["model_matrix"], 1):
        selected = deepcopy(request)
        selected["model_matrix"] = [model]
        destination = directory / f"model-{index}"
        try:
            remaining = None if time_budget is None else time_budget - (time.monotonic() - started)
            decision = invoke_harness(selected, adapter_config, destination, execution_timeout=remaining)
        except (OSError, ValueError) as error:
            raise EvidenceError(f"Comparison failed for {model}; evidence retained at {directory}: {error}") from error
        scorecards[model] = {"normalized_metrics": decision["metrics"]}
        runs[model] = str(destination)
        manifest = load_asset(destination / "run_manifest.json")
        if "total_cost" in manifest:
            costs[model] = manifest["total_cost"]
        if cost_budget is not None and (model not in costs or math.fsum(costs.values()) > cost_budget):
            raise EvidenceError(f"Comparison exceeds the shared suite cost budget; evidence retained at {directory}")
        if time_budget is not None and time.monotonic() - started > time_budget:
            raise EvidenceError(f"Comparison exceeds the shared suite time budget; evidence retained at {directory}")
    result = {"status": "pass", **aggregate_scorecards(request["suite_id"], scorecards), "runs": runs}
    result["comparison_tradeoffs"]["cost"].update(costs)
    if len(costs) == len(runs):
        result["total_cost"] = math.fsum(costs.values())
    validate_asset(result, "comparison-scorecard")
    import json
    (directory / "comparison.json").write_text(json.dumps(result, indent=2, allow_nan=False) + "\n", encoding="utf-8")
    return result
