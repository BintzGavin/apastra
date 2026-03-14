#!/bin/bash

TARGET_FILE=$1

if [ -z "$TARGET_FILE" ]; then
  echo "Usage: $0 <eval.yaml>"
  exit 1
fi

if [ ! -f "$TARGET_FILE" ]; then
  echo "Target file not found: $TARGET_FILE"
  exit 1
fi

QUICK_EVAL_SCHEMA="promptops/schemas/quick-eval.schema.json"

echo "Validating quick eval: $TARGET_FILE"
npx ajv-cli validate -s "$QUICK_EVAL_SCHEMA" -r "promptops/schemas/dataset-case.schema.json" -d "$TARGET_FILE" --spec=draft2020 --strict=false

if [ $? -ne 0 ]; then
  echo "Validation failed."
  exit 1
fi

echo "Validation passed."
exit 0
