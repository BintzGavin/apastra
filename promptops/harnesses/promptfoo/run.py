"""Execute Promptfoo and score retained responses for Apastra inline quick evals."""

import argparse
from datetime import datetime, timezone
import hashlib
import json
import math
from pathlib import Path
import re
import subprocess
import sys
import time

import jsonschema

if __package__ in (None, ""):
    import importlib
    package = Path(__file__).resolve().parents[2]
    sys.path.insert(0, str(package.parent))
    sys.modules.setdefault("promptops", importlib.import_module(package.name))

from promptops.runtime.digest import parse_json, read_json
from promptops.runtime.evidence import EvidenceError, finite_number, validate_request
from promptops.runs.evaluate_assertions import evaluate_assertions


TESTED_VERSION = "0.124.1"
DEFINITION = {"version": "1.0.0", "direction": "higher_is_better", "unit": "ratio"}
TEXT_ASSERTIONS = {"equals", "contains", "icontains", "contains-any", "contains-all", "regex", "starts-with"}
JSON_ASSERTIONS = {"is-json", "contains-json", "is-valid-json-schema"}


def _schema(value):
    if not isinstance(value, (dict, bool)):
        raise EvidenceError("JSON-schema assertion needs a schema object or boolean")
    def check_references(node):
        if isinstance(node, dict):
            if any(key in node and (not isinstance(node[key], str) or not node[key].startswith("#")) for key in ("$ref", "$dynamicRef")):
                raise EvidenceError("JSON-schema assertions cannot retrieve external references")
            for item in node.values():
                check_references(item)
        elif isinstance(node, list):
            for item in node:
                check_references(item)
    check_references(value)
    if isinstance(value, dict) and value.get("$schema", "https://json-schema.org/draft/2020-12/schema") != "https://json-schema.org/draft/2020-12/schema":
        raise EvidenceError("Only JSON Schema draft 2020-12 assertions are supported")
    try:
        jsonschema.Draft202012Validator.check_schema(value)
    except jsonschema.SchemaError as error:
        raise EvidenceError("Invalid JSON-schema assertion") from error
    return jsonschema.Draft202012Validator(value)


def _assertion_kind(assertion):
    if not isinstance(assertion, dict) or set(assertion) - {"type", "value"}:
        raise EvidenceError("Unsupported assertion fields or thresholds")
    kind = assertion.get("type", "")
    if not isinstance(kind, str):
        raise EvidenceError("Assertion type must be a string")
    base = kind.removeprefix("not-")
    if base not in TEXT_ASSERTIONS | JSON_ASSERTIONS:
        raise EvidenceError("Unsupported assertion: only deterministic response assertions are supported")
    value = assertion.get("value")
    if base in TEXT_ASSERTIONS:
        if base in {"contains-any", "contains-all"}:
            if not isinstance(value, list) or not value or any(not isinstance(item, str) for item in value):
                raise EvidenceError("Contains-list assertion needs a nonempty string list")
        elif not isinstance(value, str):
            raise EvidenceError("Text assertion value must be a string")
        if base == "regex":
            try:
                re.compile(value)
            except re.error as error:
                raise EvidenceError("Invalid regex assertion") from error
    elif base == "is-valid-json-schema":
        _schema(value)
    elif "value" in assertion:
        raise EvidenceError("JSON presence assertions do not take a value")
    return base, kind.startswith("not-"), value


def score_assertions(assertions, output):
    if not isinstance(output, str) or not isinstance(assertions, list) or not assertions:
        raise EvidenceError("String response and nonempty inline assertions are required")
    for assertion in assertions:
        _assertion_kind(assertion)
    results = evaluate_assertions(output, assertions)
    if not isinstance(results, list) or len(results) != len(assertions):
        raise EvidenceError("Built-in assertion evaluator returned incomplete results")
    scores = []
    for assertion, result in zip(assertions, results):
        key = "assert_" + assertion["type"]
        if not isinstance(result, dict) or set(result) != {key} or not finite_number(result[key]) or result[key] not in (0, 1):
            raise EvidenceError("Built-in assertion evaluation failed or returned an invalid score")
        scores.append(result[key])
    return float(all(score == 1 for score in scores))


def validate_supported_request(request):
    validate_request(request)
    if request["harness_version"] != "1.0.0":
        raise EvidenceError("Promptfoo adapter supports only harness version 1.0.0")
    evaluator = {"id": "inline-assertions-v2", "type": "deterministic", "metrics": ["pass_rate"], "metric_definitions": {"pass_rate": DEFINITION}, "config": {"source": "case.assert", "aggregation": "all assertions pass per trial; mean across trials"}}
    if request["evaluators"] != [evaluator] or not request["suite"].get("extensions", {}).get("quick_eval_digest"):
        raise EvidenceError("Promptfoo adapter supports only Apastra inline quick-eval pass_rate requests")
    if request["sampling_config"] or request["budgets"]:
        raise EvidenceError("Promptfoo adapter does not support sampling options or run budgets")
    if set(request["timeouts"]) - {"run"}:
        raise EvidenceError("Promptfoo adapter supports only the run timeout")
    template = request["prompt"]["template"]
    if not isinstance(template, str):
        raise EvidenceError("Promptfoo quick-eval prompt must be a string")
    variables = set(re.findall(r"{{\s*([A-Za-z_][A-Za-z_0-9]*)\s*}}", template))
    remainder = re.sub(r"{{\s*[A-Za-z_][A-Za-z_0-9]*\s*}}", "", template)
    if "{{" in remainder or "}}" in remainder or "{%" in template or "{#" in template:
        raise EvidenceError("Only simple quick-eval variable substitution is supported")
    for source in request["cases"]:
        if set(source["inputs"]) != variables or any(not isinstance(value, str) for value in source["inputs"].values()):
            raise EvidenceError("Promptfoo quick-eval inputs must exactly supply string prompt variables")
        if not source.get("assert"):
            raise EvidenceError("Every case needs inline assertions")
        for assertion in source["assert"]:
            _assertion_kind(assertion)


def build_config(request, model):
    validate_supported_request(request)
    if model not in request["model_matrix"]:
        raise EvidenceError("Model is not part of the requested matrix")
    provider = model
    if model.startswith("file://"):
        path = Path(model.removeprefix("file://"))
        if path.suffix != ".py" or not path.is_file():
            raise EvidenceError("Local Promptfoo providers must be explicit Python files")
        provider = "file://" + str(path.resolve())
    tests = []
    for source in request["cases"]:
        rendered = re.sub(r"{{\s*([A-Za-z_][A-Za-z_0-9]*)\s*}}", lambda match: source["inputs"][match[1]], request["prompt"]["template"])
        if rendered.startswith("file://"):
            raise EvidenceError("Rendered prompt cannot be interpreted as a Promptfoo file reference")
        for trial in range(1, request["trials"] + 1):
            tests.append({"vars": {"apastra_rendered_prompt": rendered}, "metadata": {"apastra_case_id": source["case_id"], "apastra_trial_id": trial}, "options": {"disableVarExpansion": True, "disableConversationVar": True}})
    return {"prompts": ["{{apastra_rendered_prompt}}"], "providers": [{"id": provider, "label": model}], "tests": tests, "evaluateOptions": {"maxConcurrency": 1, "repeat": 1, "cache": False}, "sharing": False}


def _total_cost(costs):
    if any(cost is None for cost in costs):
        return None
    try:
        total = math.fsum(costs)
    except OverflowError as error:
        raise EvidenceError("Promptfoo total measured cost overflowed") from error
    if not finite_number(total):
        raise EvidenceError("Promptfoo total measured cost must be finite")
    return total


def parse_results(request, model, rows):
    config = build_config(request, model)
    expected = config["tests"]
    cases = {source["case_id"]: {"case_id": source["case_id"], "model_id": model, "per_trial_outputs": []} for source in request["cases"]}
    assertions = {source["case_id"]: source["assert"] for source in request["cases"]}
    seen = set()
    costs = []
    if not isinstance(rows, list):
        raise EvidenceError("Promptfoo export must contain result rows")
    for row in rows:
        if not isinstance(row, dict):
            raise EvidenceError("Promptfoo export row must be an object")
        index = row.get("testIdx")
        if type(index) is not int or index < 0 or index >= len(expected) or index in seen or type(row.get("promptIdx")) is not int or row["promptIdx"] != 0:
            raise EvidenceError("Missing, duplicate, or unexpected Promptfoo test/prompt index")
        test = expected[index]
        response = row.get("response")
        if row.get("success") is not True or "error" in row or not isinstance(response, dict) or "error" in response or response.get("cached") is not False or not isinstance(response.get("output"), str):
            raise EvidenceError("Promptfoo provider failed, returned unsupported output, or used cached evidence")
        if any(not isinstance(row.get(key), dict) for key in ("provider", "testCase", "prompt")):
            raise EvidenceError("Promptfoo result identity fields must be objects")
        if row.get("provider", {}).get("label") != model or row.get("testCase", {}).get("metadata") != test["metadata"] or row.get("vars") != test["vars"] or row.get("prompt", {}).get("raw") != test["vars"]["apastra_rendered_prompt"]:
            raise EvidenceError("Promptfoo result does not match the requested model, case, trial, or prompt")
        cost = response.get("cost")
        if cost is not None and (not finite_number(cost) or cost < 0):
            raise EvidenceError("Promptfoo returned invalid measured cost")
        if "cost" in row and (not finite_number(row["cost"]) or row["cost"] < 0 or cost is not None and row["cost"] != cost):
            raise EvidenceError("Promptfoo returned inconsistent measured cost")
        costs.append(cost)
        case_id = test["metadata"]["apastra_case_id"]
        cases[case_id]["per_trial_outputs"].append({"trial_id": test["metadata"]["apastra_trial_id"], "output": response["output"], "evaluator_outputs": {"pass_rate": score_assertions(assertions[case_id], response["output"])}})
        seen.add(index)
    if seen != set(range(len(expected))):
        raise EvidenceError("Promptfoo export has incomplete case/trial coverage")
    for case in cases.values():
        case["per_trial_outputs"].sort(key=lambda item: item["trial_id"])
    return list(cases.values()), _total_cost(costs)


def _write_json(path, data):
    with path.open("x", encoding="utf-8") as handle:
        json.dump(data, handle, allow_nan=False)
        handle.write("\n")


def execute(request_path, output_dir, executable="promptfoo"):
    request = read_json(request_path)
    validate_supported_request(request)
    destination = Path(output_dir)
    if destination.is_symlink() or not destination.is_dir():
        raise EvidenceError("A safe existing output directory is required")
    destination = destination.resolve()
    snapshot = destination / "run_request.json"
    if not snapshot.is_file() or snapshot.is_symlink() or read_json(snapshot) != request:
        raise EvidenceError("Output directory needs the unchanged run request snapshot")
    if any(path.name != "run_request.json" for path in destination.iterdir()):
        raise EvidenceError("Adapter output directory must contain only the run request")
    raw = destination / "promptfoo"
    raw.mkdir()
    (raw / "empty.env").write_text("", encoding="utf-8")
    timeout = request["timeouts"].get("run", 300)
    started = datetime.now(timezone.utc).isoformat()
    deadline = time.monotonic() + timeout
    version = subprocess.run([executable, "--version"], cwd=raw, capture_output=True, text=True, timeout=max(0.001, deadline - time.monotonic()))
    if version.returncode or version.stdout.strip() != TESTED_VERSION:
        raise EvidenceError("Promptfoo executable must be the tested version " + TESTED_VERSION)
    cases = []
    costs = []
    references = {}
    for index, model in enumerate(request["model_matrix"], 1):
        config = build_config(request, model)
        config_path = raw / f"model-{index}.json"
        export_path = raw / f"model-{index}.jsonl"
        _write_json(config_path, config)
        command = [executable, "eval", "--config", str(config_path), "--output", str(export_path), "--no-cache", "--no-write", "--no-share", "--no-table", "--no-progress-bar", "--env-file", str(raw / "empty.env")]
        result = subprocess.run(command, cwd=raw, capture_output=True, text=True, timeout=max(0.001, deadline - time.monotonic()))
        if result.returncode:
            raise EvidenceError("Promptfoo execution or provider failed")
        if not export_path.is_file() or export_path.is_symlink() or config_path.is_symlink() or read_json(config_path) != config:
            raise EvidenceError("Missing or altered Promptfoo raw evidence")
        rows = [parse_json(line) for line in export_path.read_text(encoding="utf-8").splitlines() if line.strip()]
        model_cases, cost = parse_results(request, model, rows)
        cases.extend(model_cases)
        costs.append(cost)
        for path in (config_path, export_path):
            references[path.stem + path.suffix.replace(".", "_")] = {"uri": path.relative_to(destination).as_posix(), "digest": "sha256:" + hashlib.sha256(path.read_bytes()).hexdigest()}
    metrics = [trial["evaluator_outputs"]["pass_rate"] for case in cases for trial in case["per_trial_outputs"]]
    manifest = {"input_refs": {}, "resolved_digests": {key: request[key] for key in ("prompt_digest", "dataset_digest", "evaluator_digest", "suite_digest")}, "timestamps": {"started_at": started, "completed_at": datetime.now(timezone.utc).isoformat()}, "harness_identifier": "promptfoo", "harness_version": request["harness_version"], "model_ids": request["model_matrix"], "sampling_config": {}, "environment": {"promptfoo_version": TESTED_VERSION}, "execution_mode": "measured", "status": "completed"}
    total_cost = _total_cost(costs)
    if total_cost is not None:
        manifest["total_cost"] = total_cost
    _write_json(destination / "run_manifest.json", manifest)
    _write_json(destination / "scorecard.json", {"normalized_metrics": {"pass_rate": math.fsum(metrics) / len(metrics)}, "metric_definitions": request["required_metrics"]})
    _write_json(destination / "artifact_refs.json", {"references": references})
    with (destination / "cases.jsonl").open("x", encoding="utf-8") as handle:
        for case in cases:
            handle.write(json.dumps(case, allow_nan=False) + "\n")


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--promptfoo-executable", default="promptfoo")
    parser.add_argument("run_request")
    parser.add_argument("output_dir")
    args = parser.parse_args(argv)
    try:
        execute(args.run_request, args.output_dir, args.promptfoo_executable)
    except (OSError, ValueError, TypeError, KeyError, subprocess.TimeoutExpired) as error:
        print(json.dumps({"status": "error", "reason": "Promptfoo execution timed out" if isinstance(error, subprocess.TimeoutExpired) else str(error)}), file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
