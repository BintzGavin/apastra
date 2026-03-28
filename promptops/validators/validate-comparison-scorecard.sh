#!/bin/bash

SCHEMA_PATH="promptops/schemas/comparison-scorecard.schema.json"

if [ -z "$1" ]; then
  echo "Usage: $0 <comparison-scorecard-file>"
  exit 1
fi

DATA_FILE=$1

if [ ! -f "$DATA_FILE" ]; then
  echo "Error: File $DATA_FILE not found."
  exit 1
fi

echo "Validating $DATA_FILE against $SCHEMA_PATH..."
npx ajv-cli validate -s "$SCHEMA_PATH" -d "$DATA_FILE" --strict=false

if [ $? -eq 0 ]; then
  echo "Valid comparison scorecard."
else
  echo "Validation failed."
  exit 1
fi
