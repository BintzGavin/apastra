#!/bin/bash
set -euo pipefail

if [ "$#" -ne 1 ]; then
    echo "Usage: $0 <file>"
    exit 1
fi

FILE=$1
PYTHON_BIN="${PYTHON:-python3}"

if [ ! -f "$FILE" ]; then
    echo "Error: File '$FILE' not found."
    exit 1
fi

"$PYTHON_BIN" - "$FILE" <<'PY'
import hashlib
import json
import sys
from pathlib import Path

import yaml


def canonical_json(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


path = Path(sys.argv[1])
suffix = path.suffix.lower()

try:
    if suffix in (".yaml", ".yml"):
        with path.open("r", encoding="utf-8") as handle:
            canonical = canonical_json(yaml.safe_load(handle))
    elif suffix == ".json":
        with path.open("r", encoding="utf-8") as handle:
            canonical = canonical_json(json.load(handle))
    elif suffix == ".jsonl":
        lines = []
        with path.open("r", encoding="utf-8") as handle:
            for line in handle:
                if line.strip():
                    lines.append(canonical_json(json.loads(line)))
        canonical = "\n".join(lines)
    else:
        raise ValueError(f"Unsupported file extension '{suffix.lstrip('.')}'")
except Exception as error:
    print(f"Error: {error}", file=sys.stderr)
    sys.exit(1)

print("sha256:" + hashlib.sha256(canonical.encode("utf-8")).hexdigest())
PY
