#!/bin/bash
if [ -z "$1" ]; then
  echo "Usage: $0 <record.json>"
else
  npx ajv-cli validate --spec=draft2020 --strict=false -c ajv-formats -s promptops/schemas/reject-record.schema.json -d "$1"
fi
