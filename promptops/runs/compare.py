import json
import sys
import yaml

def load_json(path):
    with open(path, 'r') as f:
        return json.load(f)

def load_yaml(path):
    with open(path, 'r') as f:
        return yaml.safe_load(f)

def write_json(data, path):
    with open(path, 'w') as f:
        json.dump(data, f, indent=2)

def main():
    if len(sys.argv) != 5:
        print("Usage: compare.py <candidate> <baseline> <policy> <output>")
        sys.exit(1)

    candidate_path = sys.argv[1]
    baseline_path = sys.argv[2]
    policy_path = sys.argv[3]
    output_path = sys.argv[4]

    try:
        candidate = load_json(candidate_path)
        baseline = load_json(baseline_path)
    except FileNotFoundError as e:
        print(f"Error loading file: {e}")
        sys.exit(1)

    policy = load_yaml(policy_path)

    candidate_metrics = candidate.get("normalized_metrics", {})
    baseline_metrics = baseline.get("normalized_metrics", {})

    status = "pass"
    evidence = []
    has_blocker = False
    has_warning = False

    ruled_metrics = set()
    for rule in policy.get("rules", []):
        metric = rule["metric"]
        severity = rule["severity"]
        floor = rule.get("floor")
        allowed_delta = rule.get("allowed_delta")
        direction = rule.get("direction")

        c_val = candidate_metrics.get(metric)
        b_val = baseline_metrics.get(metric)

        if c_val is None or b_val is None:
            evidence.append({
                "metric": metric,
                "candidate_value": c_val,
                "baseline_value": b_val,
                "status": "fail",
                "message": "Metric missing in candidate or baseline."
            })
            if severity == "blocker": has_blocker = True
            if severity == "warning": has_warning = True
            continue

        delta = c_val - b_val
        passed = True
        message = ""

        if direction == "higher_is_better":
            if floor is not None and c_val < floor:
                passed = False
                message = f"Value {c_val} below floor {floor}."
            elif allowed_delta is not None and c_val < (b_val - allowed_delta):
                passed = False
                message = f"Delta {delta} exceeds allowed drop {allowed_delta}."
        elif direction == "lower_is_better":
            if floor is not None and c_val > floor:
                passed = False
                message = f"Value {c_val} above ceiling {floor}."
            elif allowed_delta is not None and c_val > (b_val + allowed_delta):
                passed = False
                message = f"Delta {delta} exceeds allowed rise {allowed_delta}."

        ruled_metrics.add(metric)
        evidence.append({
            "metric": metric,
            "candidate_value": c_val,
            "baseline_value": b_val,
            "delta": delta,
            "status": "pass" if passed else "fail",
            "message": message
        })

        if not passed:
            if severity == "blocker": has_blocker = True
            if severity == "warning": has_warning = True

    all_metrics = set(candidate_metrics.keys()).union(set(baseline_metrics.keys()))
    ungated_metrics = all_metrics - ruled_metrics

    for metric in ungated_metrics:
        c_val = candidate_metrics.get(metric)
        b_val = baseline_metrics.get(metric)
        if c_val is not None and b_val is not None:
            delta = c_val - b_val
            evidence.append({
                "metric": metric,
                "candidate_value": c_val,
                "baseline_value": b_val,
                "delta": delta,
                "status": "info",
                "message": ""
            })
        else:
            evidence.append({
                "metric": metric,
                "candidate_value": c_val,
                "baseline_value": b_val,
                "status": "info",
                "message": "Metric missing in candidate or baseline."
            })

    if has_blocker:
        status = "fail"
    elif has_warning:
        status = "warning"

    report = {
        "status": status,
        "baseline_ref": baseline_path,
        "candidate_ref": candidate_path,
        "evidence": evidence
    }

    write_json(report, output_path)
    print(f"Report written to {output_path}")

if __name__ == "__main__":
    main()
