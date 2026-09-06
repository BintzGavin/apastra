"""Versioned, strict semantic identities for JSON, YAML, and JSONL assets."""

import hashlib
import json
import math
from pathlib import Path
import sys

import yaml


def unique_object(pairs):
    result = {}
    for key, value in pairs:
        if not isinstance(key, str) or key in result:
            raise ValueError("Asset keys must be unique strings")
        result[key] = value
    return result


def invalid_constant(_value):
    raise ValueError("Nonfinite numbers are not valid asset data")


class StrictLoader(yaml.SafeLoader):
    pass


def _yaml_mapping(loader, node):
    return unique_object((loader.construct_object(key), loader.construct_object(value)) for key, value in node.value)


StrictLoader.add_constructor(yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG, _yaml_mapping)


def parse_json(text):
    return json.loads(text, object_pairs_hook=unique_object, parse_constant=invalid_constant)


def _normalize(value):
    if isinstance(value, dict):
        if any(not isinstance(key, str) for key in value):
            raise ValueError("Asset keys must be strings")
        return {key: _normalize(item) for key, item in value.items()}
    if isinstance(value, list):
        return [_normalize(item) for item in value]
    if type(value) is float:
        if not math.isfinite(value):
            raise ValueError("Nonfinite numbers are not valid asset data")
        return int(value) if value.is_integer() else value
    if value is None or type(value) in (str, int, bool):
        return value
    raise ValueError("Assets must contain JSON-compatible values")


def canonical_json(value):
    return json.dumps(_normalize(value), sort_keys=True, separators=(",", ":"), ensure_ascii=False, allow_nan=False)


def load_asset(file_path):
    path = Path(file_path)
    text = path.read_text(encoding="utf-8")
    if path.suffix in (".yaml", ".yml"):
        data = yaml.load(text, Loader=StrictLoader)
    elif path.suffix == ".json":
        data = parse_json(text)
    elif path.suffix == ".jsonl":
        data = [parse_json(line) for line in text.splitlines() if line.strip()]
    else:
        raise ValueError("Unsupported asset extension")
    return _normalize(data)


def read_json(file_path):
    return _normalize(parse_json(Path(file_path).read_text(encoding="utf-8")))


def compute_digest(file_path):
    path = Path(file_path)
    data = load_asset(path)
    canonical = "\n".join(canonical_json(row) for row in data) if path.suffix == ".jsonl" else canonical_json(data)
    return "sha256:" + hashlib.sha256(canonical.encode("utf-8")).hexdigest()


def compute_digest_from_dict(data):
    if not isinstance(data, dict):
        raise ValueError("Expected an object")
    return "sha256:" + hashlib.sha256(canonical_json(data).encode("utf-8")).hexdigest()


def asset_group_digest(kind, paths):
    digests = [compute_digest(path) for path in paths]
    return group_digest(kind, digests)


def group_digest(kind, digests):
    if not digests:
        raise ValueError("An asset group cannot be empty")
    if len(digests) == 1:
        return digests[0]
    return compute_digest_from_dict({"domain": "apastra:asset-group:v2", "kind": kind, "digests": digests})


def dataset_digest(cases):
    canonical = "\n".join(canonical_json(case) for case in cases)
    return "sha256:" + hashlib.sha256(canonical.encode("utf-8")).hexdigest()


if __name__ == "__main__":
    try:
        if len(sys.argv) != 2:
            raise ValueError("Usage: digest.py <asset.json|yaml|jsonl>")
        print(compute_digest(sys.argv[1]))
    except (OSError, ValueError, yaml.YAMLError) as error:
        print(str(error), file=sys.stderr)
        raise SystemExit(1)
