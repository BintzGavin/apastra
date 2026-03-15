#!/bin/bash
npx ajv-cli validate -s promptops/schemas/submission-record.schema.json -d "$1" --spec=draft2020 --strict=false -c ajv-formats
if [ $? -eq 0 ]; then
  echo "$1 is valid"
  exit 0
else
  exit 1
fi
