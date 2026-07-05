import os
import json
import glob
import hashlib
import shutil
import subprocess
import sys
import tempfile
import yaml
from pathlib import PurePosixPath

try:
    from mcp.server.fastmcp import FastMCP
except ImportError:
    class FastMCP:
        def __init__(self, name):
            self.name = name

        def tool(self):
            def decorator(func):
                return func
            return decorator

        def run(self):
            raise RuntimeError(
                "The optional 'mcp' package is required to start the Apastra MCP server."
            )

mcp = FastMCP("promptops")

TEXT_EXTENSIONS = (".yaml", ".yml", ".json", ".jsonl", ".txt", ".md")

class UnsafeReferenceError(ValueError):
    pass

def _json_response(payload):
    return json.dumps(payload, sort_keys=True)

def _validate_local_ref(ref, label):
    if not isinstance(ref, str) or not ref.strip():
        raise UnsafeReferenceError(f"{label} must be a non-empty string")
    if "\\" in ref:
        raise UnsafeReferenceError(f"Unsafe {label}: {ref}")

    path = PurePosixPath(ref)
    if path.is_absolute() or any(part in ("", ".", "..") for part in path.parts):
        raise UnsafeReferenceError(f"Unsafe {label}: {ref}")
    return ref

def _validate_ref_list(refs, label):
    if isinstance(refs, str):
        refs = [refs]
    refs = refs or []
    return [_validate_local_ref(ref, label) for ref in refs]

def _sha256_text(value):
    return "sha256:" + hashlib.sha256(value.encode("utf-8")).hexdigest()

def _sha256_file(path):
    with open(path, "rb") as f:
        return "sha256:" + hashlib.sha256(f.read()).hexdigest()

def _load_structured_file(path):
    with open(path, "r", encoding="utf-8") as f:
        if path.endswith((".yaml", ".yml")):
            return yaml.safe_load(f) or {}
        return json.load(f)

def _suite_files():
    files = (
        glob.glob("promptops/suites/*.yaml")
        + glob.glob("promptops/suites/*.yml")
        + glob.glob("promptops/suites/*.json")
    )
    if not files:
        files = (
            glob.glob("suites/*.yaml")
            + glob.glob("suites/*.yml")
            + glob.glob("suites/*.json")
        )
    return files

def _find_first_existing(paths):
    for path in paths:
        if os.path.exists(path):
            return path
    return None

def _suite_path(suite_id):
    suite_id = _validate_local_ref(suite_id, "suite_id")
    direct = _find_first_existing([
        f"promptops/suites/{suite_id}.yaml",
        f"promptops/suites/{suite_id}.yml",
        f"promptops/suites/{suite_id}.json",
        f"suites/{suite_id}.yaml",
        f"suites/{suite_id}.yml",
        f"suites/{suite_id}.json",
    ])
    if direct:
        return direct

    for suite_file in _suite_files():
        try:
            data = _load_structured_file(suite_file)
        except (OSError, json.JSONDecodeError, yaml.YAMLError):
            continue
        if data.get("id") == suite_id:
            return suite_file
    return None

def _structured_file_has_id(path, ref):
    if not path.endswith((".yaml", ".yml", ".json")):
        return False
    try:
        data = _load_structured_file(path)
    except (OSError, json.JSONDecodeError, yaml.YAMLError):
        return False
    return data.get("id") == ref

def _scan_assets_for_id(kind, ref):
    patterns = [
        f"promptops/{kind}/*.yaml",
        f"promptops/{kind}/*.yml",
        f"promptops/{kind}/*.json",
        f"{kind}/*.yaml",
        f"{kind}/*.yml",
        f"{kind}/*.json",
    ]
    if kind == "datasets":
        patterns.extend([
            f"promptops/{kind}/*/dataset-manifest.yaml",
            f"promptops/{kind}/*/dataset-manifest.yml",
            f"{kind}/*/dataset-manifest.yaml",
            f"{kind}/*/dataset-manifest.yml",
        ])
    if kind == "prompts":
        patterns.extend([
            f"promptops/{kind}/*/prompt.yaml",
            f"promptops/{kind}/*/prompt.yml",
            f"promptops/{kind}/*/prompt.json",
            f"{kind}/*/prompt.yaml",
            f"{kind}/*/prompt.yml",
            f"{kind}/*/prompt.json",
        ])

    for pattern in patterns:
        for path in glob.glob(pattern):
            if _structured_file_has_id(path, ref):
                return path
    return None

def _candidate_asset_paths(kind, ref):
    ref = _validate_local_ref(ref, f"{kind} reference")

    bases = [f"promptops/{kind}", kind]
    candidates = []
    has_extension = os.path.splitext(ref)[1] != ""
    if has_extension:
        candidates.append(ref)
        for base in bases:
            candidates.append(os.path.join(base, ref))
    else:
        extensions = {
            "prompts": (".yaml", ".yml", ".json"),
            "datasets": (".jsonl", ".json", ".yaml", ".yml"),
            "evaluators": (".yaml", ".yml", ".json"),
        }.get(kind, TEXT_EXTENSIONS)

        for base in bases:
            for extension in extensions:
                candidates.append(os.path.join(base, ref + extension))
            if kind == "datasets":
                candidates.append(os.path.join(base, ref, "dataset.jsonl"))
                candidates.append(os.path.join(base, ref, "dataset.json"))
                candidates.append(os.path.join(base, ref, "dataset.yaml"))
                candidates.append(os.path.join(base, ref, "dataset.yml"))
                candidates.append(os.path.join(base, ref, "dataset-manifest.yaml"))
                candidates.append(os.path.join(base, ref, "dataset-manifest.yml"))
            if kind == "prompts":
                candidates.append(os.path.join(base, ref, "prompt.yaml"))
                candidates.append(os.path.join(base, ref, "prompt.yml"))
                candidates.append(os.path.join(base, ref, "prompt.json"))

    return candidates

def _resolve_asset(kind, ref):
    return _find_first_existing(_candidate_asset_paths(kind, ref)) or _scan_assets_for_id(
        kind,
        ref,
    )

def _digest_refs(kind, refs):
    refs = _validate_ref_list(refs, f"{kind} reference")

    paths = []
    missing = []
    for ref in refs:
        path = _resolve_asset(kind, ref)
        if path:
            paths.append(path)
        else:
            missing.append(ref)

    if missing:
        raise FileNotFoundError(
            f"Missing {kind} asset(s): {', '.join(str(ref) for ref in missing)}"
        )

    if not paths:
        return _sha256_text(""), []

    if len(paths) == 1:
        return _sha256_file(paths[0]), paths

    digest = hashlib.sha256()
    for path in paths:
        digest.update(path.encode("utf-8"))
        digest.update(b"\0")
        with open(path, "rb") as f:
            digest.update(f.read())
        digest.update(b"\0")
    return "sha256:" + digest.hexdigest(), paths

def _cleanup_paths(*paths):
    errors = []
    for path in paths:
        if not path:
            continue
        try:
            if os.path.isdir(path):
                shutil.rmtree(path)
            elif os.path.exists(path):
                os.remove(path)
        except OSError as error:
            errors.append(f"{path}: {error}")
    return errors

@mcp.tool()
def list_suites() -> list:
    """Lists available evaluation suites in the current workspace."""
    suites = []
    for suite_file in _suite_files():
        try:
            data = _load_structured_file(suite_file)
            if data and "id" in data:
                suites.append({
                    "id": data["id"],
                    "name": data.get("name", ""),
                    "description": data.get("description", "")
                })
        except (OSError, json.JSONDecodeError, yaml.YAMLError) as error:
            print(
                f"Warning: failed to load suite file {suite_file}: {error}",
                file=sys.stderr,
            )
    return suites

@mcp.tool()
def run_evaluation(suite_id: str, revision_ref: str = "latest") -> str:
    """Runs a PromptOps evaluation suite.

    Args:
        suite_id: The ID of the evaluation suite to run.
        revision_ref: The reference to test against (e.g. latest, commit sha).
    """
    try:
        suite_file = _suite_path(suite_id)
    except UnsafeReferenceError as error:
        return _json_response({
            "status": "error",
            "reason": "unsafe_ref",
            "message": str(error),
            "suite_id": str(suite_id),
        })

    if not suite_file:
        return _json_response({
            "status": "error",
            "reason": "suite_not_found",
            "message": f"Suite not found: {suite_id}",
            "suite_id": suite_id,
        })

    try:
        data = _load_structured_file(suite_file)
    except (OSError, json.JSONDecodeError, yaml.YAMLError) as error:
        return _json_response({
            "status": "error",
            "reason": "invalid_suite",
            "message": f"Failed to load suite {suite_id}",
            "error": str(error),
            "suite_id": suite_id,
        })

    prompt_ref = data.get("prompt")
    dataset_refs = data.get("datasets", [])
    evaluator_refs = data.get("evaluators", [])

    try:
        prompt_d, prompt_paths = _digest_refs(
            "prompts",
            [prompt_ref] if prompt_ref else [],
        )
        dataset_d, dataset_paths = _digest_refs("datasets", dataset_refs)
        evaluator_d, evaluator_paths = _digest_refs("evaluators", evaluator_refs)
    except UnsafeReferenceError as error:
        return _json_response({
            "status": "error",
            "reason": "unsafe_ref",
            "message": str(error),
            "suite_id": str(suite_id),
        })
    except FileNotFoundError as error:
        return _json_response({
            "status": "error",
            "reason": "asset_not_found",
            "message": str(error),
            "suite_id": suite_id,
        })

    run_request = {
        "suite_id": suite_id,
        "revision_ref": revision_ref,
        "model_matrix": data.get("model_matrix", ["default"]),
        "evaluator_refs": evaluator_refs,
        "dataset_refs": dataset_refs,
        "prompt_ref": prompt_ref,
        "prompt_digest": prompt_d,
        "dataset_digest": dataset_d,
        "evaluator_digest": evaluator_d,
        "suite_digest": _sha256_file(suite_file),
        "harness_version": "1.0.0"
    }

    with tempfile.NamedTemporaryFile('w', delete=False, suffix='.json') as f:
        json.dump(run_request, f)
        req_path = f.name

    out_dir = tempfile.mkdtemp()

    adapter_path = "promptops/harnesses/reference-adapter/adapter.yaml"
    if not os.path.exists(adapter_path):
        adapter_path = "harnesses/reference-adapter/adapter.yaml"

    if not os.path.exists(adapter_path):
        _cleanup_paths(req_path, out_dir)
        return _json_response({
            "status": "error",
            "reason": "adapter_not_found",
            "message": f"Harness adapter config not found. Could not run suite {suite_id}",
            "suite_id": suite_id
        })

    cmd = [
        sys.executable,
        "-m",
        "promptops.runtime.runner",
        req_path,
        adapter_path,
        out_dir,
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)

    if result.returncode != 0:
        cleanup_errors = _cleanup_paths(req_path, out_dir)

        return _json_response({
            "status": "error",
            "reason": "execution_failed",
            "message": f"Execution failed for suite {suite_id}",
            "error": result.stderr or result.stdout,
            "cleanup_errors": cleanup_errors,
        })

    try:
        scorecard_path = os.path.join(out_dir, "scorecard.json")
        scorecard_data = None
        if os.path.exists(scorecard_path):
            with open(scorecard_path, 'r') as sf:
                scorecard_data = json.load(sf)

        cleanup_errors = _cleanup_paths(req_path, out_dir)

        if scorecard_data:
            return _json_response({
                "status": "success",
                "message": f"Execution completed for suite {suite_id}",
                "scorecard": scorecard_data,
                "digests": {
                    "prompt_digest": prompt_d,
                    "dataset_digest": dataset_d,
                    "evaluator_digest": evaluator_d,
                },
                "resolved_assets": {
                    "prompt": prompt_paths,
                    "datasets": dataset_paths,
                    "evaluators": evaluator_paths,
                },
                "cleanup_errors": cleanup_errors,
            })
    except (OSError, json.JSONDecodeError) as error:
        cleanup_errors = _cleanup_paths(req_path, out_dir)
        return _json_response({
            "status": "error",
            "reason": "scorecard_read_failed",
            "message": f"Execution completed for suite {suite_id}, but scorecard could not be read",
            "error": str(error),
            "cleanup_errors": cleanup_errors,
        })

    cleanup_errors = _cleanup_paths(req_path, out_dir)
    return _json_response({
        "status": "error",
        "reason": "scorecard_not_found",
        "message": f"Execution completed for suite {suite_id}, but scorecard not found",
        "cleanup_errors": cleanup_errors,
    })

def start_mcp_server():
    mcp.run()
