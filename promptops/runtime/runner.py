"""Invoke a declared harness and admit only complete measured evidence."""

import argparse
from copy import deepcopy
import json
from pathlib import Path
import shlex
import subprocess
import sys

import yaml

if __package__ in (None, ""):
    import importlib
    package = Path(__file__).resolve().parents[1]
    sys.path.insert(0, str(package.parent))
    sys.modules.setdefault("promptops", importlib.import_module(package.name))

from promptops.runtime.evidence import EvidenceError, finite_number, read_json, validate_evidence, validate_request
from promptops.runtime.digest import compute_digest_from_dict, load_asset


def run(request_path, adapter_path, output_dir, execution_timeout=None, cwd=None):
    request = deepcopy(request_path) if isinstance(request_path, dict) else read_json(request_path)
    from promptops.runtime.suite import validate_asset
    validate_request(request)
    adapter = load_asset(adapter_path)
    validate_asset(adapter, "harness-adapter")
    if not isinstance(adapter, dict) or adapter.get("execution_mode") != "measured":
        raise EvidenceError("Unsupported harness: configure an explicit measured execution adapter")
    entrypoint = adapter.get("entrypoint")
    if not isinstance(entrypoint, str) or not entrypoint.strip():
        raise EvidenceError("Harness entrypoint is required")
    if "run_suite" not in adapter["capabilities"] or adapter.get("version") != request["harness_version"]:
        raise EvidenceError("Adapter must declare run_suite capability and the requested harness version")
    timeout = request.get("timeouts", {}).get("run", 300)
    if "time" in request.get("budgets", {}):
        timeout = min(timeout, request["budgets"]["time"])
    if not finite_number(timeout) or timeout <= 0:
        raise EvidenceError("Run timeout must be a positive number of seconds")
    if execution_timeout is not None:
        if not finite_number(execution_timeout) or execution_timeout <= 0:
            raise EvidenceError("Comparison time budget exhausted")
        timeout = min(timeout, execution_timeout)
    directory = Path(output_dir).resolve()
    directory.mkdir(parents=True, exist_ok=True)
    if any(directory.iterdir()):
        raise EvidenceError("Output directory must be empty; existing evidence is never overwritten")
    snapshot = directory / "run_request.json"
    snapshot.write_text(json.dumps(request, sort_keys=True, allow_nan=False), encoding="utf-8")
    command = shlex.split(entrypoint) + [str(snapshot), str(directory)]
    try:
        result = subprocess.run(command, capture_output=True, text=True, timeout=timeout, cwd=cwd)
    except subprocess.TimeoutExpired as error:
        raise EvidenceError("Harness execution timed out") from error
    if result.returncode:
        return {"status": "error", "reason": "harness_failed", "exit_code": result.returncode}
    if read_json(snapshot) != request:
        raise EvidenceError("Harness modified the admitted run request")
    decision = validate_evidence(request, directory)
    if read_json(directory / "run_manifest.json")["harness_identifier"] != adapter["id"]:
        raise EvidenceError("Harness identity does not match the invoked adapter")
    invocation = {"adapter_digest": compute_digest_from_dict(adapter), "adapter_id": adapter["id"], "adapter_version": adapter["version"], "request_digest": decision["request_digest"], "exit_code": 0}
    (directory / "invocation.json").write_text(json.dumps(invocation, indent=2) + "\n", encoding="utf-8")
    decision["invocation_digest"] = compute_digest_from_dict(invocation)
    (directory / "evaluation.json").write_text(json.dumps(decision, indent=2, allow_nan=False) + "\n", encoding="utf-8")
    return decision


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("run_request")
    parser.add_argument("adapter")
    parser.add_argument("output_dir")
    args = parser.parse_args(argv)
    try:
        decision = run(args.run_request, args.adapter, args.output_dir)
    except (OSError, ValueError, TypeError, KeyError, yaml.YAMLError) as error:
        print(json.dumps({"status": "error", "reason": str(error)}), file=sys.stderr)
        return 1
    print(json.dumps(decision, sort_keys=True))
    return 0 if decision["status"] == "pass" else decision.get("exit_code", 2)


if __name__ == "__main__":
    raise SystemExit(main())
