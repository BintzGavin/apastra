"""Aggregate complete per-trial evidence with declared metric semantics."""

import argparse
from copy import deepcopy
import json
import math
from pathlib import Path
import sys

if __package__ in (None, ""):
    import importlib
    package = Path(__file__).resolve().parents[1]
    sys.path.insert(0, str(package.parent))
    sys.modules.setdefault("promptops", importlib.import_module(package.name))

from promptops.runtime.digest import load_asset
from promptops.runtime.evidence import EvidenceError, finite_number
from promptops.runtime.suite import validate_asset


def normalize_scorecard(cases, definitions=None):
    if not cases or not definitions:
        raise EvidenceError("Normalization requires cases and explicit metric definitions")
    values = {name: [] for name in definitions}
    seen = set()
    trial_count = None
    for case in cases:
        validate_asset(case, "run-case")
        key = (case["model_id"], case["case_id"])
        if key in seen:
            raise EvidenceError("Duplicate model/case evidence")
        seen.add(key)
        outputs = case["per_trial_outputs"]
        trial_count = len(outputs) if trial_count is None else trial_count
        if not trial_count or len(outputs) != trial_count or {row["trial_id"] for row in outputs} != set(range(1, trial_count + 1)):
            raise EvidenceError("Incomplete or duplicate trial coverage")
        for row in outputs:
            scores = row["evaluator_outputs"]
            if set(scores) != set(definitions) or any(not finite_number(value) for value in scores.values()):
                raise EvidenceError("Every trial must supply every declared finite metric")
            for name, value in scores.items():
                values[name].append(value)
    means = {name: math.fsum(scores) / len(scores) for name, scores in values.items()}
    result = {
        "normalized_metrics": means,
        "metric_definitions": deepcopy(definitions),
        "variance": {name: math.fsum((value - means[name]) ** 2 for value in scores) / len(scores) for name, scores in values.items()},
    }
    validate_asset(result, "scorecard")
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("cases")
    parser.add_argument("definitions", help="JSON metric-definition map")
    parser.add_argument("output")
    args = parser.parse_args()
    try:
        result = normalize_scorecard(load_asset(args.cases), load_asset(args.definitions))
        with Path(args.output).open("x", encoding="utf-8") as handle:
            json.dump(result, handle, indent=2, allow_nan=False)
    except (OSError, ValueError, TypeError, KeyError) as error:
        print(json.dumps({"status": "error", "reason": str(error)}), file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
