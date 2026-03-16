#!/bin/bash

FILE=$1
if [ -z "$FILE" ]; then
  echo "Usage: $0 <moderation-decision-record.json|yaml>"
  exit 1
fi

npx ajv-cli validate -s promptops/schemas/moderation-decision-record.schema.json -d "$FILE" -c ajv-formats
