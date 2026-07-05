#!/bin/bash
set -euo pipefail

if [ "$#" -ne 3 ]; then
    echo "Usage: $0 <adapter_yaml> <run_request> <output_dir>"
    exit 1
fi

ADAPTER_YAML=$1
RUN_REQUEST=$2
OUTPUT_DIR=$3
PYTHON_BIN="${PYTHON:-python3}"

if [ ! -f "$ADAPTER_YAML" ]; then
    echo "Error: Adapter YAML not found at $ADAPTER_YAML"
    exit 1
fi

if [ ! -f "$RUN_REQUEST" ]; then
    echo "Error: Run request not found at $RUN_REQUEST"
    exit 1
fi

ENTRYPOINT=$("$PYTHON_BIN" - "$ADAPTER_YAML" <<'PY'
import sys

import yaml

with open(sys.argv[1], "r", encoding="utf-8") as handle:
    data = yaml.safe_load(handle) or {}

entrypoint = data.get("entrypoint", "")
if entrypoint is None:
    entrypoint = ""
print(entrypoint)
PY
)

if [ -z "$ENTRYPOINT" ] || [ "$ENTRYPOINT" == "null" ]; then
    echo "Error: Could not extract entrypoint from $ADAPTER_YAML"
    exit 1
fi

mkdir -p "$OUTPUT_DIR"

echo "Executing harness entrypoint: $ENTRYPOINT $RUN_REQUEST $OUTPUT_DIR"
$ENTRYPOINT "$RUN_REQUEST" "$OUTPUT_DIR"

if [ ! -f "$OUTPUT_DIR/run_manifest.json" ]; then
    echo "Warning: run_manifest.json not found in output directory"
fi

echo "Harness execution complete. Artifacts collected in $OUTPUT_DIR"
