#!/bin/bash
if [ "$#" -ne 1 ]; then
    echo "Usage: $0 <policy-exception-record.json|yaml>"
    exit 1
fi

INPUT_FILE="$1"
TMP_FILE=$(mktemp --suffix=.json)
python3 -c 'import sys, yaml, json; json.dump(yaml.safe_load(sys.stdin), sys.stdout)' < "$INPUT_FILE" > "$TMP_FILE"

if ajv validate -c ajv-formats -s promptops/schemas/policy-exception-record.schema.json -d "$TMP_FILE"; then
    rm -f "$TMP_FILE"
    exit 0
else
    rm -f "$TMP_FILE"
    exit 1
fi