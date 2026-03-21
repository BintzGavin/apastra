#!/bin/bash
set -e

SCHEMA_FILE="$(dirname "$0")/../schemas/provenance-attestation.schema.json"

if [ -z "$1" ]; then
    echo "Usage: $0 <file.json>"
    exit 1
fi

if ! command -v ajv >/dev/null 2>&1; then
    echo "ajv-cli not found. Ensure it is installed."
    exit 1
fi

TMP_FILE=$(mktemp --suffix=.json)
python3 -c 'import sys, yaml, json; json.dump(yaml.safe_load(sys.stdin), sys.stdout)' < "$1" > "$TMP_FILE"

if ajv validate -c ajv-formats -s "$SCHEMA_FILE" -d "$TMP_FILE"; then
    echo "Validation successful."
    rm -f "$TMP_FILE"
    exit 0
else
    echo "Validation failed."
    rm -f "$TMP_FILE"
    exit 1
fi
