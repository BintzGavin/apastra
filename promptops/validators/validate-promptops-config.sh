#!/bin/bash
set -e
if [ "$#" -ne 1 ]; then
    echo "Usage: $0 <file>"
    exit 1
fi
ajv validate -s promptops/schemas/promptops-config.schema.json -d "$1"
