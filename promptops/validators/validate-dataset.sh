#!/bin/bash

# 1. Take input arguments: path to manifest (YAML/JSON) and path to cases (JSONL).
MANIFEST_FILE=$1
CASES_FILE=$2

if [ -z "$MANIFEST_FILE" ] || [ -z "$CASES_FILE" ]; then
  echo "Usage: $0 <manifest.json|yaml> <cases.jsonl>"
  exit 1
fi

if [ ! -f "$MANIFEST_FILE" ]; then
  echo "Manifest file not found: $MANIFEST_FILE"
  exit 1
fi

if [ ! -f "$CASES_FILE" ]; then
  echo "Cases file not found: $CASES_FILE"
  exit 1
fi

MANIFEST_SCHEMA="promptops/schemas/dataset-manifest.schema.json"
CASE_SCHEMA="promptops/schemas/dataset-case.schema.json"

# 2. Convert manifest YAML to JSON (ajv-cli parses YAML natively)
# 3. Run ajv-cli against dataset-manifest.schema.json with the manifest file.
echo "Validating manifest: $MANIFEST_FILE"
npx ajv-cli validate -s "$MANIFEST_SCHEMA" -d "$MANIFEST_FILE" --spec=draft2020 --strict=false

if [ $? -ne 0 ]; then
  echo "Manifest validation failed."
  exit 1
fi

echo "Manifest validation passed."

# 4. For each line in the cases JSONL file:
echo "Validating cases in: $CASES_FILE"
LINE_NUM=1
VALIDATION_FAILED=0

# Create a temporary directory for single JSON line files
TMP_DIR=$(mktemp -d)

while IFS= read -r line; do
  # Skip empty lines
  if [ -z "$line" ]; then
    ((LINE_NUM++))
    continue
  fi

  # Write the line to a temporary file
  TMP_FILE="$TMP_DIR/line_$LINE_NUM.json"
  echo "$line" > "$TMP_FILE"

  # 5. Run ajv-cli against promptops/schemas/dataset-case.schema.json.
  # Capture output to avoid noisy success messages for every single line
  OUTPUT=$(npx ajv-cli validate -s "$CASE_SCHEMA" -d "$TMP_FILE" --spec=draft2020 --strict=false 2>&1)

  if [ $? -ne 0 ]; then
    echo "Validation failed at line $LINE_NUM:"
    echo "$OUTPUT"
    VALIDATION_FAILED=1
  fi

  ((LINE_NUM++))
done < "$CASES_FILE"

# Clean up temporary directory
rm -rf "$TMP_DIR"

# 6. Exit 0 if all validations succeed; exit 1 and print errors on failure.
if [ $VALIDATION_FAILED -ne 0 ]; then
  echo "Case validation failed."
  exit 1
fi

echo "All test cases validation passed."
exit 0
