#!/bin/bash
if [ "$#" -ne 1 ]; then
    echo "Usage: $0 <policy-exception-record.json|yaml>"
    exit 1
fi

TMP_FILE=$(mktemp --suffix=.json)
python3 -c 'import sys, yaml, json; json.dump(yaml.safe_load(sys.stdin), sys.stdout)' < "$1" > "$TMP_FILE"

if ! ajv validate -c ajv-formats -s promptops/schemas/policy-exception-record.schema.json -d "$TMP_FILE"; then
    echo "Validation failed."
    rm -f "$TMP_FILE"
    exit 1
fi

echo "Validation successful."
rm -f "$TMP_FILE"
exit 0