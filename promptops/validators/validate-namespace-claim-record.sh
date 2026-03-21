#!/usr/bin/env bash
set -e

SCHEMA_FILE="promptops/schemas/namespace-claim-record.schema.json"

if [ "$#" -ne 1 ]; then
    echo "Usage: $0 <namespace_claim_record_file.json_or_yaml>"
    exit 1
fi

if [ ! -f "$1" ]; then
    echo "Error: File '$1' not found."
    exit 1
fi

echo "Validating $1 against $SCHEMA_FILE..."

# Convert YAML/JSON to a temporary JSON file, then validate using ajv
# Use a specific suffix .json so ajv understands it correctly
TMP_FILE=$(mktemp --suffix=.json)
python3 -c 'import sys, yaml, json; json.dump(yaml.safe_load(sys.stdin), sys.stdout)' < "$1" > "$TMP_FILE"

if ajv validate -c ajv-formats -s "$SCHEMA_FILE" -d "$TMP_FILE"; then
    echo "Validation successful!"
    rm -f "$TMP_FILE"
    exit 0
else
    echo "Validation failed!"
    rm -f "$TMP_FILE"
    exit 1
fi
