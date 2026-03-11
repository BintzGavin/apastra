#!/bin/bash
SCHEMA_PATH="promptops/schemas/artifact-refs.schema.json"
if [ -z "$1" ]; then
  echo "Usage: $0 <artifact-refs.json>"
  exit 1
fi
TARGET_FILE="$1"
if [ ! -f "$TARGET_FILE" ]; then
  echo "Error: File '$TARGET_FILE' not found."
  exit 1
fi
echo "Validating '$TARGET_FILE' against '$SCHEMA_PATH'..."
npx ajv-cli validate -s "$SCHEMA_PATH" -d "$TARGET_FILE" --spec=draft2020 --strict=false
STATUS=$?
if [ $STATUS -eq 0 ]; then
  echo "Validation successful!"
  exit 0
else
  echo "Validation failed."
  exit 1
fi
