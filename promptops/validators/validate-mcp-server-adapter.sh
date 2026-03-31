#!/bin/bash

SCHEMA_PATH="promptops/schemas/mcp-server-adapter.schema.json"

if [ -z "$1" ]; then
  echo "Usage: $0 <mcp-server-adapter-file>"
  exit 1
fi

TARGET_FILE="$1"

if [ ! -f "$TARGET_FILE" ]; then
  echo "Error: File '$TARGET_FILE' not found."
  exit 1
fi

echo "Validating '$TARGET_FILE' against '$SCHEMA_PATH'..."
if [[ "$TARGET_FILE" == *.yaml ]] || [[ "$TARGET_FILE" == *.yml ]]; then
    TMP_JSON=$(mktemp)
    yq . "$TARGET_FILE" > "$TMP_JSON"
    npx ajv-cli validate -s "$SCHEMA_PATH" -d "$TMP_JSON" --spec=draft2020 --strict=false
    STATUS=$?
    rm "$TMP_JSON"
else
    npx ajv-cli validate -s "$SCHEMA_PATH" -d "$TARGET_FILE" --spec=draft2020 --strict=false
    STATUS=$?
fi

if [ $STATUS -eq 0 ]; then
  echo "Validation successful!"
  exit 0
else
  echo "Validation failed."
  exit 1
fi