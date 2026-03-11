import json
import sys

def normalize_scorecard(cases):
    if not cases:
        return {
            "normalized_metrics": {},
            "metric_definitions": {}
        }

    metrics_sum = {}
    metrics_count = {}

    for case in cases:
        for eval_output in case.get("evaluator_outputs", []):
            for key, value in eval_output.items():
                if isinstance(value, (int, float)):
                    metrics_sum[key] = metrics_sum.get(key, 0) + value
                    metrics_count[key] = metrics_count.get(key, 0) + 1

    normalized_metrics = {}
    metric_definitions = {}

    for key, count in metrics_count.items():
        normalized_metrics[key] = metrics_sum[key] / count
        metric_definitions[key] = {
            "type": "float",
            "range": [0, 1] if normalized_metrics[key] <= 1.0 else [0, None]
        }

    return {
        "normalized_metrics": normalized_metrics,
        "metric_definitions": metric_definitions
    }

def main():
    if len(sys.argv) != 2:
        print("Usage: python normalize.py <run_artifact.json>")
        sys.exit(1)

    artifact_path = sys.argv[1]

    with open(artifact_path, 'r') as f:
        artifact = json.load(f)

    cases = artifact.get("cases", [])
    scorecard = normalize_scorecard(cases)

    artifact["scorecard"] = scorecard

    with open(artifact_path, 'w') as f:
        json.dump(artifact, f, indent=2)

if __name__ == "__main__":
    main()
