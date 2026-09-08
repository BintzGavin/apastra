"""Resolve a suite once for CLI, MCP, and multi-model execution."""

from copy import deepcopy
from functools import lru_cache
from pathlib import Path, PurePosixPath
import subprocess
import uuid

import jsonschema
from referencing import Registry, Resource

from promptops.runtime.digest import asset_group_digest, compute_digest, load_asset
from promptops.runtime.evidence import EvidenceError


class UnsafeReferenceError(EvidenceError):
    pass


def safe_reference(ref):
    if not isinstance(ref, str) or not ref or "\\" in ref:
        raise UnsafeReferenceError("Asset reference must be a nonempty relative path or ID")
    path = PurePosixPath(ref)
    if path.is_absolute() or any(part in (".", "..", "") for part in ref.split("/")):
        raise UnsafeReferenceError("Asset reference escapes its asset directory")
    return ref


def asset_directory(kind, workspace=None):
    root = Path(workspace) if workspace is not None else Path(".")
    primary = root / "promptops" / kind
    return primary if workspace is not None or primary.is_dir() else root / kind


def resolve_asset(kind, ref, workspace=None):
    safe_reference(ref)
    base = asset_directory(kind, workspace).resolve()
    if workspace is not None and not base.is_relative_to(Path(workspace).resolve()):
        raise UnsafeReferenceError("Asset directory escapes workspace")
    candidates = [base / ref]
    if not Path(ref).suffix:
        candidates += [base / (ref + suffix) for suffix in (".jsonl", ".json", ".yaml", ".yml")]
        if kind == "datasets":
            candidates += [base / ref / name for name in ("dataset.jsonl", "cases.jsonl")]
        if kind == "prompts":
            candidates += [base / ref / name for name in ("prompt.json", "prompt.yaml", "prompt.yml")]
    for path in candidates:
        if not path.resolve().is_relative_to(base):
            raise UnsafeReferenceError("Asset symlink escapes its asset directory")
        if path.is_file():
            return path
    matches = []
    for path in sorted(base.rglob("*")):
        if path.suffix not in (".json", ".yaml", ".yml") or not path.is_file():
            continue
        if not path.resolve().is_relative_to(base):
            continue
        data = load_asset(path)
        if isinstance(data, dict) and data.get("id") == ref:
            matches.append(path)
    if len(matches) > 1:
        raise EvidenceError(f"Ambiguous {kind} ID: {ref}")
    if not matches:
        raise FileNotFoundError(f"{kind} asset not found: {ref}")
    path = matches[0]
    if kind == "datasets":
        for candidate in (path.with_name(path.name.split(".manifest")[0] + ".jsonl"), path.parent / "dataset.jsonl", path.parent / "cases.jsonl"):
            if candidate.is_file() and candidate.resolve().is_relative_to(base):
                return candidate
        raise EvidenceError("Dataset manifest has no corresponding JSONL cases")
    return path


@lru_cache(maxsize=1)
def schema_registry():
    schemas = {path.name.removesuffix(".schema.json"): load_asset(path) for path in (Path(__file__).resolve().parents[1] / "schemas").glob("*.schema.json")}
    registry = Registry().with_resources((schema["$id"], Resource.from_contents(schema)) for schema in schemas.values() if "$id" in schema)
    return schemas, registry


def validate_asset(data, kind):
    schemas, registry = schema_registry()
    if kind not in schemas:
        raise EvidenceError("Unknown asset schema")
    try:
        jsonschema.Draft202012Validator(schemas[kind], registry=registry, format_checker=jsonschema.FormatChecker()).validate(data)
    except jsonschema.ValidationError as error:
        location = ".".join(map(str, error.absolute_path)) or "root"
        raise EvidenceError(f"Invalid {kind}: {error.validator} at {location}") from error


def load_suite(suite_id, workspace=None):
    path = resolve_asset("suites", suite_id, workspace)
    suite = load_asset(path)
    if not isinstance(suite, dict):
        raise EvidenceError("Suite must be an object")
    for kind in ("datasets", "evaluators"):
        for ref in suite.get(kind, []):
            safe_reference(ref)
    validate_asset(suite, "suite")
    return suite, path


def build_request(suite_id, models=None, revision_ref="workspace", harness_version="1.0.0", workspace=None):
    if revision_ref not in ("workspace", "latest"):
        raise EvidenceError("Historical revision execution is unsupported; check out the revision and evaluate the workspace")
    suite, suite_path = load_suite(suite_id, workspace)
    if not suite.get("prompt"):
        raise EvidenceError("Suite must declare its prompt")
    prompt_path = resolve_asset("prompts", suite["prompt"], workspace)
    prompt = load_asset(prompt_path)
    validate_asset(prompt, "prompt-spec")
    dataset_paths = [resolve_asset("datasets", ref, workspace) for ref in suite["datasets"]]
    evaluator_paths = [resolve_asset("evaluators", ref, workspace) for ref in suite["evaluators"]]
    cases = []
    for path in dataset_paths:
        if path.suffix != ".jsonl":
            raise EvidenceError("Dataset cases must be JSONL")
        for case in load_asset(path):
            validate_asset(case, "dataset-case")
            variables = {"type": "object", "properties": prompt["variables"], "required": list(prompt["variables"]), "additionalProperties": False}
            try:
                jsonschema.validate(case["inputs"], variables)
            except jsonschema.ValidationError as error:
                raise EvidenceError(f"Dataset inputs do not match prompt variables: {case['case_id']}") from error
            cases.append(case)
    case_ids = [case["case_id"] for case in cases]
    if not cases or len(set(case_ids)) != len(case_ids):
        raise EvidenceError("Dataset case IDs must be nonempty and unique across the suite")
    metrics = {}
    evaluators = []
    for path in evaluator_paths:
        evaluator = load_asset(path)
        validate_asset(evaluator, "evaluator")
        definitions = evaluator.get("metric_definitions", {})
        if set(definitions) != set(evaluator["metrics"]):
            raise EvidenceError("Evaluator must define every metric's version, direction, and unit")
        if set(metrics) & set(definitions):
            raise EvidenceError("Evaluator metric names must be unique across the suite")
        metrics.update(definitions)
        evaluators.append(evaluator)
    selected_models = models if models is not None else suite["model_matrix"]
    if not selected_models or any(not isinstance(model, str) or not model for model in selected_models) or len(set(selected_models)) != len(selected_models):
        raise EvidenceError("Model selection must be nonempty and unique")
    source = subprocess.run(["git", "rev-parse", "HEAD"], capture_output=True, text=True, cwd=workspace)
    request = {
        "suite_id": suite["id"], "revision_ref": "workspace",
        "requested_revision": revision_ref,
        "source_revision": source.stdout.strip() if source.returncode == 0 else None,
        "model_matrix": selected_models, "evaluator_refs": suite["evaluators"],
        "prompt_digest": compute_digest(prompt_path),
        "dataset_digest": asset_group_digest("datasets", dataset_paths),
        "evaluator_digest": asset_group_digest("evaluators", evaluator_paths),
        "suite_digest": compute_digest(suite_path), "harness_version": harness_version,
        "expected_case_ids": case_ids, "required_metrics": metrics,
        "trials": suite.get("trials", 1), "thresholds": suite.get("thresholds", {}),
        "budgets": suite.get("budgets", {}), "timeouts": suite.get("timeouts", {}),
        "sampling_config": suite.get("sampling_config", {}),
        "prompt": prompt, "cases": cases, "datasets": [load_asset(path) for path in dataset_paths], "evaluators": evaluators,
        "suite": deepcopy(suite),
    }
    return request


def evaluate_suite(suite_id, adapter_config=None, output_dir=None, revision_ref="workspace", models=None):
    # Resolve unsafe/missing suite references before returning a capability error.
    load_suite(suite_id)
    if not adapter_config:
        return {"status": "unsupported", "reason": "adapter_required"}
    request = build_request(suite_id, models, revision_ref, harness_version=load_asset(adapter_config).get("version"))
    directory = Path(output_dir or Path("promptops/runs") / f"eval-{uuid.uuid4().hex}").resolve()
    from promptops.runtime.runner import run
    result = run(request, adapter_config, directory)
    return {**result, "output_dir": str(directory)}
