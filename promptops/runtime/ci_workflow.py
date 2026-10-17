"""GitHub Actions wiring for revision-bound admission and changed-asset validation."""

import argparse
import json
from pathlib import Path
import re
import subprocess

from promptops.runtime.ci import ci_gate
from promptops.runtime.dataset import validate_dataset
from promptops.runtime.digest import load_asset
from promptops.runtime.evidence import EvidenceError
from promptops.runtime.gate import resolve_baseline
from promptops.runtime.suite import safe_reference, validate_asset


INPUT_GROUPS = {"prompts", "datasets", "evaluators", "suites", "evals", "policies", "harnesses", "runtime", "schemas", "validators", "baselines", "resolver", "runs", "hooks", "request_log", "integrations"}
ASSET_KINDS = {"prompts": "prompt-spec", "evaluators": "evaluator", "suites": "suite", "evals": "quick-eval", "policies": "regression-policy", "harnesses": "harness-adapter", "baselines": "baseline"}


CODE_SUFFIXES = {".py", ".sh", ".js", ".mjs", ".cjs", ".ts", ".tsx", ".jsx"}
CONFIG_SUFFIXES = {".json", ".yaml", ".yml", ".toml", ".cfg", ".ini", ".lock"}
ROOT_CONFIG_FILES = {"setup", "Pipfile", "Dockerfile", "Makefile", ".npmrc", ".nvmrc", ".node-version", ".python-version"}
RETAINED_RUN_FILES = {"run_request.json", "run_manifest.json", "scorecard.json", "cases.jsonl", "artifact_refs.json", "evaluation.json", "invocation.json", "comparison.json"}


def _product_parts(path):
    parts = Path(path).parts
    if parts[:3] == (".agent", "scripts", "apastra"):
        return ("promptops", *parts[3:])
    if parts[:2] == (".agent", "runtime"):
        return ("promptops", *parts[1:])
    return parts


def _asset_group(path):
    parts = _product_parts(path)
    if len(parts) >= 3 and parts[:2] == ("derived-index", "baselines"):
        return "baselines"
    if len(parts) >= 3 and parts[0] == "promptops" and parts[1] in {*ASSET_KINDS, "datasets"}:
        return parts[1]
    return None


def relevant_change(path):
    parts = _product_parts(path)
    suffix = Path(path).suffix
    if not parts or suffix in {".md", ".rst"}:
        return False
    if parts[:2] == ("derived-index", "baselines"):
        return True
    if len(parts) > 1 and parts[0] == "promptops":
        if parts[1] == "tests":
            return False
        # Retained run artifacts do not change executable or evaluation inputs.
        if parts[1] == "runs" and len(parts) >= 4 and parts[-1] in RETAINED_RUN_FILES:
            return False
        return parts[1] in INPUT_GROUPS or suffix in CODE_SUFFIXES | CONFIG_SUFFIXES
    if parts[0] in {"docs", "tests"}:
        return False
    if parts[0] in {"bin", "scripts"}:
        return True
    if parts[0] in {".agent", ".github", "setup-ci"}:
        return suffix in CODE_SUFFIXES | CONFIG_SUFFIXES or parts[:2] == (".agent", "bin")
    return len(parts) == 1 and (parts[0] in ROOT_CONFIG_FILES or suffix in CODE_SUFFIXES | CONFIG_SUFFIXES or (parts[0].startswith("requirements") and suffix in {".txt", ".in"}))


def _requires_full_validation(path):
    return relevant_change(path) and (_asset_group(path) is None or Path(path).suffix in CODE_SUFFIXES)


def _all_asset_paths():
    roots = [base / group for base in (Path("promptops"), Path(".agent/scripts/apastra")) for group in {*ASSET_KINDS, "datasets"}]
    roots.append(Path("derived-index/baselines"))
    return [path.as_posix() for root in roots for path in root.rglob("*") if path.is_file()]


def _git(*arguments):
    result = subprocess.run(["git", *arguments], capture_output=True)
    if result.returncode:
        raise EvidenceError("Cannot determine checked-out CI revision or changed inputs")
    return result.stdout


def changed_paths(base, revision):
    if not all(isinstance(value, str) and re.fullmatch(r"[0-9a-f]{40}|[0-9a-f]{64}", value) for value in (base, revision)):
        raise EvidenceError("CI needs explicit full base and tested revision SHAs")
    if _git("rev-parse", "HEAD").decode().strip() != revision:
        raise EvidenceError("CI checkout does not match the expected revision")
    return [path.decode("utf-8") for path in _git("diff", "--name-only", "--no-renames", "-z", base, revision, "--").split(b"\0") if path]


def workspace_path(value):
    safe_reference(value)
    path = Path(value)
    if not path.resolve().is_relative_to(Path.cwd().resolve()):
        raise EvidenceError("CI path escapes the checkout")
    return path


def workflow_gate(base, revision, suite, adapter, mode, run_dir, baseline=None, policy=None):
    if not any(relevant_change(path) for path in changed_paths(base, revision)):
        return {"status": "pass", "reason": "No evaluation inputs changed"}
    if not all(isinstance(value, str) and value.strip() for value in (suite, adapter, mode, run_dir)):
        raise EvidenceError("Relevant changes require explicit CI suite, adapter, mode, and run directory configuration")
    safe_reference(suite)
    adapter = workspace_path(adapter)
    run_dir = workspace_path(run_dir.replace("{revision}", revision))
    if revision not in run_dir.parts:
        raise EvidenceError("CI run directory must contain the tested revision as a path component")
    baseline = workspace_path(baseline) if baseline else None
    if baseline:
        baseline_dir, _ = resolve_baseline(baseline, suite)
        if not baseline_dir.resolve().is_relative_to(Path.cwd().resolve()):
            raise EvidenceError("CI baseline evidence escapes the checkout")
    policy = workspace_path(policy) if policy else None
    return ci_gate(suite, adapter, revision, mode, run_dir, baseline, policy)


def _dataset_cases(manifest):
    candidates = {manifest.with_suffix(".jsonl"), manifest.with_name(manifest.name.split(".manifest")[0] + ".jsonl"), manifest.parent / "dataset.jsonl", manifest.parent / "cases.jsonl"}
    matches = [path for path in candidates if path.is_file()]
    if len(matches) != 1:
        raise EvidenceError("Dataset manifest needs exactly one corresponding JSONL cases file")
    return workspace_path(matches[0].as_posix())


def _dataset_manifests(path):
    manifests = {path.with_name(path.stem + ".manifest" + suffix) for suffix in (".json", ".yaml", ".yml")}
    if path.name in {"dataset.jsonl", "cases.jsonl"}:
        manifests |= {path.parent / (name + suffix) for name in ("manifest", "dataset-manifest") for suffix in (".json", ".yaml", ".yml")}
    return [manifest for manifest in manifests if manifest.is_file()]


def _validate_dataset(path):
    if path.suffix != ".jsonl":
        return validate_dataset(path, _dataset_cases(path))
    existing = _dataset_manifests(path)
    if len(existing) > 1:
        raise EvidenceError("Dataset has ambiguous manifests")
    if existing:
        return validate_dataset(workspace_path(existing[0].as_posix()), path)
    cases = load_asset(path)
    if not cases:
        raise EvidenceError("Dataset must contain at least one case")
    for case in cases:
        validate_asset(case, "dataset-case")
    if len({case["case_id"] for case in cases}) != len(cases):
        raise EvidenceError("Dataset case IDs must be unique")


def validate_assets(paths):
    count = 0
    for relative in sorted(set(paths)):
        group = _asset_group(relative)
        if group is None or Path(relative).suffix not in {".json", ".yaml", ".yml", ".jsonl"}:
            continue
        path = workspace_path(relative)
        if not path.is_file():
            # A retained manifest cannot silently lose its cases on deletion.
            if group == "datasets" and path.suffix == ".jsonl" and _dataset_manifests(path):
                _validate_dataset(path)
            # Other deleted assets have no current schema; the gate requires fresh evidence.
            continue
        if group == "datasets":
            _validate_dataset(path)
        else:
            data = load_asset(path)
            kind = "prompt-package" if group == "prompts" and isinstance(data, dict) and "specs" in data else ASSET_KINDS[group]
            validate_asset(data, kind)
        count += 1
    return {"status": "pass", "validated_assets": count}


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)
    gate = subparsers.add_parser("gate")
    assets = subparsers.add_parser("validate-assets")
    for command in (gate, assets):
        command.add_argument("--base", required=True)
        command.add_argument("--revision", required=True)
    for option in ("suite", "adapter", "mode", "run-dir", "baseline", "policy"):
        gate.add_argument("--" + option, default="")
    args = parser.parse_args(argv)
    if args.command == "gate":
        result = workflow_gate(args.base, args.revision, args.suite, args.adapter, args.mode, args.run_dir, args.baseline, args.policy)
    else:
        paths = changed_paths(args.base, args.revision)
        if any(_requires_full_validation(path) for path in paths):
            paths = _all_asset_paths()
        result = validate_assets(paths)
    print(json.dumps(result, allow_nan=False))
    return 0 if result["status"] == "pass" else 2
