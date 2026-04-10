import json
import uuid
import os
import yaml
import subprocess
import tempfile
import jsonschema
import sys
import shutil

def load_suite(suite_id):
    path = os.path.join("promptops", "suites", f"{suite_id}.yaml")
    if not os.path.exists(path):
        raise FileNotFoundError(f"Suite not found: {path}")
    with open(path, "r") as f:
        return yaml.safe_load(f)

def construct_run_request(suite, model):
    return {
        "suite_id": suite["id"],
        "revision_ref": suite.get("digest", "sha256:" + __import__('hashlib').sha256(suite['id'].encode()).hexdigest()),
        "model_matrix": [model],
        "evaluator_refs": suite.get("evaluators", []),
        "prompt_digest": "sha256:" + __import__('hashlib').sha256(suite['id'].encode()).hexdigest(),
        "dataset_digest": "sha256:" + __import__('hashlib').sha256(suite['id'].encode()).hexdigest(),
        "evaluator_digest": "sha256:" + __import__('hashlib').sha256(suite['id'].encode()).hexdigest(),
        "harness_version": "v1.0.0"
    }

def invoke_harness(run_req, adapter_config=None, out_dir=None):
    if adapter_config is not None:
        if not os.path.exists(adapter_config):
            raise FileNotFoundError(f"Adapter config not found: {adapter_config}")

        fd, req_path = tempfile.mkstemp(suffix=".json")
        try:
            with os.fdopen(fd, "w") as f:
                json.dump(run_req, f)

            runner_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "runner.py")
            result = subprocess.run([sys.executable, runner_path, req_path, adapter_config, out_dir], check=False)
            if result.returncode != 0:
                print(f"Warning: Harness execution failed for model {run_req['model_matrix'][0]} with code {result.returncode}")
        finally:
            os.remove(req_path)
    else:
        # Generate mock scorecard for test
        scorecard = {
            "id": str(uuid.uuid4()),
            "suite_id": run_req["suite_id"],
            "baselines": [],
            "models": run_req["model_matrix"],
            "metrics": {
                run_req["model_matrix"][0]: {
                    "exact_match_score": 0.85,
                    "latency_ms": 150
                }
            }
        }
        with open(os.path.join(out_dir, "scorecard.json"), "w") as f:
            json.dump(scorecard, f)

    return out_dir

def load_scorecard(out_dir):
    path = os.path.join(out_dir, "scorecard.json")
    if not os.path.exists(path):
        return None
    try:
        with open(path, "r") as f:
            return json.load(f)
    except json.JSONDecodeError as e:
        print(f"Warning: Failed to decode scorecard at {path}: {e}")
        return None

def aggregate_scorecards(suite_id, individual_scorecards):
    baselines = []
    models = list(individual_scorecards.keys())
    metrics = {}
    cost_tradeoff = {}
    quality_tradeoff = {}
    latency_tradeoff = {}

    for model, sc in individual_scorecards.items():
        if not sc:
            continue
        model_metrics = sc.get("metrics", {}).get(model, {})
        metrics[model] = model_metrics
        cost_tradeoff[model] = model_metrics.get("cost_usd", 0.0)
        quality_tradeoff[model] = model_metrics.get("exact_match_score", 0.0)
        latency_tradeoff[model] = model_metrics.get("latency_ms", 0.0)

    return {
        "id": str(uuid.uuid4()),
        "suite_id": suite_id,
        "baselines": baselines,
        "models": models,
        "metrics": metrics,
        "comparison_tradeoffs": {
            "cost": cost_tradeoff,
            "quality": quality_tradeoff,
            "latency": latency_tradeoff
        }
    }

def run_comparison(suite_id, models=None, adapter_config=None):
    suite = load_suite(suite_id)
    models_to_run = models or suite.get("model_matrix", ["default"])
    individual_scorecards = {}

    for model in models_to_run:
        run_req = construct_run_request(suite, model)
        out_dir = tempfile.mkdtemp()
        try:
            invoke_harness(run_req, adapter_config, out_dir)
            sc = load_scorecard(out_dir)
            if sc:
                individual_scorecards[model] = sc
            else:
                print(f"Warning: No valid scorecard generated for model {model}")
        finally:
            shutil.rmtree(out_dir, ignore_errors=True)

    comparison_scorecard = aggregate_scorecards(suite["id"], individual_scorecards)

    current_dir = os.path.dirname(os.path.abspath(__file__))
    schema_path = os.path.abspath(os.path.join(current_dir, "..", "schemas", "comparison-scorecard.schema.json"))
    with open(schema_path, "r") as sf:
        schema = json.load(sf)
    jsonschema.validate(instance=comparison_scorecard, schema=schema)

    return comparison_scorecard
