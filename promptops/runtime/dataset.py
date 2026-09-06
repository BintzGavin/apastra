"""Validate manifest-backed datasets, including their content identity."""

import argparse
import json
from pathlib import Path
import sys

if __package__ in (None, ""):
    import importlib
    package = Path(__file__).resolve().parents[1]
    sys.path.insert(0, str(package.parent))
    sys.modules.setdefault("promptops", importlib.import_module(package.name))

from promptops.runtime.digest import compute_digest, load_asset
from promptops.runtime.evidence import EvidenceError
from promptops.runtime.suite import validate_asset


def validate_dataset(manifest_path, cases_path):
    manifest = load_asset(manifest_path)
    validate_asset(manifest, "dataset-manifest")
    if Path(cases_path).suffix != ".jsonl":
        raise EvidenceError("Dataset cases must use JSONL")
    cases = load_asset(cases_path)
    if not cases:
        raise EvidenceError("Dataset must contain at least one case")
    for case in cases:
        validate_asset(case, "dataset-case")
    if len({case["case_id"] for case in cases}) != len(cases):
        raise EvidenceError("Dataset case IDs must be unique")
    if manifest["digest"] != compute_digest(cases_path):
        raise EvidenceError("Dataset manifest digest does not match its cases")
    return {"status": "valid", "cases": len(cases), "digest": manifest["digest"]}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("manifest")
    parser.add_argument("cases")
    args = parser.parse_args()
    try:
        print(json.dumps(validate_dataset(args.manifest, args.cases)))
        return 0
    except (OSError, ValueError, TypeError, KeyError) as error:
        print(json.dumps({"status": "error", "reason": str(error)}), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
