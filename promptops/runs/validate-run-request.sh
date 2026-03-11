#!/bin/bash
if [ -z "$1" ]; then
    echo "Usage: $0 <run-request-json>"
    exit 1
fi
npx ajv-cli validate -s promptops/schemas/run-request.schema.json -d "$1" --spec=draft2020 --strict=false