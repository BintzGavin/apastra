#!/bin/bash
if [ "$#" -ne 1 ]; then
    echo "Usage: $0 <file.json>"
    exit 1
fi
if ajv validate -c ajv-formats --spec=draft2020 -s promptops/schemas/audit-report.schema.json -d "$1"; then
    echo "Validation succeeded"
    exit 0
else
    echo "Validation failed"
    exit 1
fi