#!/bin/bash
set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
. "$SCRIPT_DIR/lib/ajv.sh"

# Validator script for evaluator specs

SCHEMA_PATH="promptops/schemas/evaluator.schema.json"

if [ -z "$1" ]; then
  echo "Usage: $0 <evaluator-spec-file>"
  exit 1
fi

TARGET_FILE="$1"

if [ ! -f "$TARGET_FILE" ]; then
  echo "Error: File '$TARGET_FILE' not found."
  exit 1
fi

echo "Validating '$TARGET_FILE' against '$SCHEMA_PATH'..."
apastra_ajv_validate "$SCHEMA_PATH" "$TARGET_FILE" --spec=draft2020 --strict=false

if [ $? -eq 0 ]; then
  echo "Validation successful!"
  exit 0
else
  echo "Validation failed."
  exit 1
fi
