import json
import hashlib
import yaml
import sys
import os

def compute_digest(file_path: str) -> str:
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")

    canonical_content = ""

    with open(file_path, 'r', encoding='utf-8') as f:
        if file_path.endswith('.yaml') or file_path.endswith('.yml'):
            data = yaml.safe_load(f)
            if data is None:
                raise ValueError("Empty YAML file")
            canonical_content = json.dumps(data, separators=(',', ':'), sort_keys=True)
        elif file_path.endswith('.json'):
            data = json.load(f)
            canonical_content = json.dumps(data, separators=(',', ':'), sort_keys=True)
        elif file_path.endswith('.jsonl'):
            lines = []
            for line in f:
                line = line.strip()
                if not line:
                    continue
                data = json.loads(line)
                lines.append(json.dumps(data, separators=(',', ':'), sort_keys=True))
            canonical_content = "\n".join(lines)
        else:
            raise ValueError("Unsupported file extension. Use .yaml, .yml, .json, or .jsonl")

    digest = hashlib.sha256(canonical_content.encode('utf-8')).hexdigest()
    return f"sha256:{digest}"

def compute_digest_from_dict(data: dict) -> str:
    if not isinstance(data, dict):
        return None
    canonical_json = json.dumps(data, separators=(',', ':'), sort_keys=True)
    digest = hashlib.sha256(canonical_json.encode('utf-8')).hexdigest()
    return f"sha256:{digest}"

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python digest.py <file_path>")
        sys.exit(1)
    try:
        print(compute_digest(sys.argv[1]))
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)
