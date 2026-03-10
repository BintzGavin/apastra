#!/bin/bash
set -e

if [ "$#" -ne 1 ]; then
    echo "Usage: $0 <consumption-manifest.yaml|json>"
    exit 1
fi

MANIFEST_FILE="$1"
SCHEMA_FILE="promptops/schemas/consumption-manifest.schema.json"

if [ ! -f "$MANIFEST_FILE" ]; then
    echo "Error: Manifest file '$MANIFEST_FILE' not found."
    exit 1
fi

if [ ! -f "$SCHEMA_FILE" ]; then
    echo "Error: Schema file '$SCHEMA_FILE' not found."
    exit 1
fi

echo "Validating '$MANIFEST_FILE' against '$SCHEMA_FILE'..."
npx ajv-cli validate -s "$SCHEMA_FILE" -d "$MANIFEST_FILE" --spec=draft2020 --strict=false

echo "Validation successful!"
