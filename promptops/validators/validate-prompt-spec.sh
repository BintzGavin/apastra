#!/bin/bash

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

# 2. Run ajv-cli against promptops/schemas/prompt-spec.schema.json
# Note: ajv-cli parses YAML natively
npx ajv-cli validate -s promptops/schemas/prompt-spec.schema.json -d "$INPUT_FILE" --spec=draft2020 --strict=false

# Capture the exit code
EXIT_CODE=$?

# 3. Exit 0 on success, exit 1 on failure
exit $EXIT_CODE
