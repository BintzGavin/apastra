#!/bin/bash
# Usage: ./validate-observability-adapter-config.sh <data-file.json>
set -e
SCHEMA="promptops/schemas/observability-adapter-config.schema.json"
DATA=$1

if [ -z "$DATA" ]; then
  echo "Error: Data file required."
  echo "Usage: $0 <data-file.json>"
  exit 1
fi

if [[ "$DATA" == *.yaml ]] || [[ "$DATA" == *.yml ]]; then
  TMP_JSON=$(mktemp --suffix=.json)
  yq . "$DATA" > "$TMP_JSON"
  npx ajv-cli validate -s "$SCHEMA" -d "$TMP_JSON" --spec=draft2020 --strict=false
  STATUS=$?
  rm "$TMP_JSON"
  exit $STATUS
else
  npx ajv-cli validate -s "$SCHEMA" -d "$DATA" --spec=draft2020 --strict=false
fi
