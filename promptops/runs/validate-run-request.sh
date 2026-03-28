#!/bin/bash
if [ -z "$1" ]; then
    echo "Usage: $0 <run-request-json>"
    exit 1
fi

# Check for required digest fields using jq before schema validation
MISSING_FIELDS=()
for field in prompt_digest dataset_digest evaluator_digest harness_version; do
    if ! jq -e "has(\"$field\")" "$1" > /dev/null; then
        MISSING_FIELDS+=("$field")
    fi
done

if [ ${#MISSING_FIELDS[@]} -ne 0 ]; then
    echo "Error: Run request is missing required fields for reproducibility:"
    printf '  - %s\n' "${MISSING_FIELDS[@]}"
    exit 1
fi

npx ajv-cli validate -s promptops/schemas/run-request.schema.json -d "$1" --spec=draft2020 --strict=false
