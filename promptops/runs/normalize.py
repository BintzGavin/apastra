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
