#!/bin/bash
set -u

if [ "$#" -ne 1 ]; then
    echo "Usage: $0 <moderation-approval-for-public-listing.json|yaml>"
    exit 1
fi

INPUT_FILE="$1"
SCHEMA_FILE="promptops/schemas/moderation-approval-for-public-listing.schema.json"

if [ ! -f "$INPUT_FILE" ]; then
    echo "Error: Input file '$INPUT_FILE' not found."
    exit 1
fi

TMP_FILE=$(mktemp --suffix=.json)
if ! python3 -c 'import sys, yaml, json; json.dump(yaml.safe_load(sys.stdin), sys.stdout)' < "$INPUT_FILE" > "$TMP_FILE" 2>/dev/null; then
    echo "Error: Failed to parse input file as JSON or YAML."
    rm -f "$TMP_FILE"
    exit 1
fi

if ajv validate -c ajv-formats --spec=draft2020 -s "$SCHEMA_FILE" -d "$TMP_FILE"; then
    rm -f "$TMP_FILE"
    exit 0
else
    rm -f "$TMP_FILE"
    exit 1
fi
