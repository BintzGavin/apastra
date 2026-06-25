#!/bin/bash
set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
. "$SCRIPT_DIR/lib/ajv.sh"

# 1. Take input file path (YAML or JSON)
INPUT_FILE=$1

if [ -z "$INPUT_FILE" ]; then
  echo "Usage: $0 <prompt-spec.json|yaml>"
  exit 1
fi

if [ ! -f "$INPUT_FILE" ]; then
  echo "File not found: $INPUT_FILE"
  exit 1
fi

# 2. Run ajv-cli against promptops/schemas/prompt-spec.schema.json.
# YAML inputs are converted explicitly before validation.
apastra_ajv_validate promptops/schemas/prompt-spec.schema.json "$INPUT_FILE" --spec=draft2020 --strict=false

# Capture the exit code
EXIT_CODE=$?

# 3. Exit 0 on success, exit 1 on failure
exit $EXIT_CODE
