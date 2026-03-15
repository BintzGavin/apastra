import json
import sys

def normalize_scorecard(cases):
    if not cases:
        return {
            "normalized_metrics": {},
            "metric_definitions": {},
            "variance": {}
        }

    metrics_sum = {}
    metrics_count = {}
    metrics_values = {}
    metric_versions = {}

    for case in cases:
        for eval_output in case.get("evaluator_outputs", []):
            extracted_version = eval_output.get("metric_version", "1.0.0")
            for key, value in eval_output.items():
                if key == "metric_version":
                    continue
                if isinstance(value, (int, float)):
                    metrics_sum[key] = metrics_sum.get(key, 0) + value
                    metrics_count[key] = metrics_count.get(key, 0) + 1
                    if key not in metrics_values:
                        metrics_values[key] = []
                        metric_versions[key] = extracted_version
                    metrics_values[key].append(value)

    normalized_metrics = {}
    metric_definitions = {}
    variance = {}

    for key, count in metrics_count.items():
        mean = metrics_sum[key] / count
        normalized_metrics[key] = mean

        var = sum((x - mean) ** 2 for x in metrics_values[key]) / count
        variance[key] = var
        metric_definitions[key] = {
            "type": "float",
            "range": [0, 1] if normalized_metrics[key] <= 1.0 else [0, None],
            "version": metric_versions.get(key, "1.0.0")
        }

    return {
        "normalized_metrics": normalized_metrics,
        "metric_definitions": metric_definitions,
        "variance": variance
    }

def main():
    if len(sys.argv) != 3:
        print("Usage: python normalize.py <cases.jsonl> <output_scorecard.json>")
        sys.exit(1)

    cases_path = sys.argv[1]
    scorecard_path = sys.argv[2]

    cases = []
    with open(cases_path, 'r') as f:
        for line in f:
            if line.strip():
                cases.append(json.loads(line))

    scorecard = normalize_scorecard(cases)

    with open(scorecard_path, 'w') as f:
        json.dump(scorecard, f, indent=2)

if __name__ == "__main__":
    main()
