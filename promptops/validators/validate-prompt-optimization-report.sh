#!/bin/bash
if [ "$#" -ne 1 ]; then
    echo "Usage: $0 <file.json>"
    exit 1
fi
if ajv validate -c ajv-formats -s promptops/schemas/prompt-optimization-report.schema.json -d "$1"; then
    echo "Validation succeeded"
    exit 0
else
    echo "Validation failed"
    exit 1
fi
