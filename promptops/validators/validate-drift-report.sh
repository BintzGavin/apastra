#!/bin/bash

# Validator script for drift-report.schema.json

if [ -z "$1" ]; then
  echo "Usage: $0 <path-to-drift-report-instance>"
  exit 1
fi

INSTANCE_FILE="$1"
SCHEMA_FILE="promptops/schemas/drift-report.schema.json"

if [ ! -f "$INSTANCE_FILE" ]; then
  echo "Error: Instance file '$INSTANCE_FILE' not found."
  exit 1
fi

if [ ! -f "$SCHEMA_FILE" ]; then
  echo "Error: Schema file '$SCHEMA_FILE' not found."
  exit 1
fi

# Run validation using ajv
ajv validate -s "$SCHEMA_FILE" -d "$INSTANCE_FILE"

# Capture the exit code of ajv
EXIT_CODE=$?

if [ $EXIT_CODE -eq 0 ]; then
  echo "Validation successful: '$INSTANCE_FILE' is a valid drift report."
else
  echo "Validation failed: '$INSTANCE_FILE' does not conform to the drift report schema."
fi

exit $EXIT_CODE
