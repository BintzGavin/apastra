#!/bin/bash
if [[ "$1" == *.yaml ]] || [[ "$1" == *.yml ]]; then
  TMP_JSON=$(mktemp --suffix=.json)
  yq . "$1" > "$TMP_JSON"
  npx ajv-cli validate -s promptops/schemas/promotion-record.schema.json -d "$TMP_JSON" --spec=draft2020 --strict=false
  STATUS=$?
  rm "$TMP_JSON"
  exit $STATUS
else
  npx ajv-cli validate -s promptops/schemas/promotion-record.schema.json -d "$1" --spec=draft2020 --strict=false
fi
