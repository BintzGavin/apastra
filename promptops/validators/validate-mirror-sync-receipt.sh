#!/bin/bash

FILE=$1
if [ -z "$FILE" ]; then
  echo "Usage: $0 <mirror-sync-receipt.json|yaml>"
  exit 1
fi

npx ajv-cli validate -s promptops/schemas/mirror-sync-receipt.schema.json -d "$FILE" -c ajv-formats
