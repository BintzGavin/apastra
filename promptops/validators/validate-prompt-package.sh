#!/bin/bash
set -e

if [ -z "$1" ]; then
  echo "Usage: $0 <prompt-package.json|yaml>"
  exit 1
fi

FILE="$1"
TEMP_FILE=""

# Check if the file is YAML and convert to JSON if necessary
if [[ "$FILE" == *.yaml || "$FILE" == *.yml ]]; then
  TEMP_FILE="$(mktemp).json"
  yq . "$FILE" > "$TEMP_FILE"
  FILE="$TEMP_FILE"
fi

# Validate the JSON file against the schema
npx ajv-cli validate -s promptops/schemas/prompt-package.schema.json -d "$FILE" --spec=draft2020 --strict=false

# Clean up temp file if created
if [ -n "$TEMP_FILE" ]; then
  rm -f "$TEMP_FILE"
fi
