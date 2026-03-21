#!/bin/bash
if [ -z "$1" ]; then
  echo "Usage: $0 <moderation-escalation-record.json|yaml>"
  exit 1
fi
TMP_FILE=$(mktemp --suffix=.json)
python3 -c 'import sys, yaml, json; json.dump(yaml.safe_load(sys.stdin), sys.stdout)' < "$1" > "$TMP_FILE"
if ajv validate -c ajv-formats --spec=draft2020 -s promptops/schemas/moderation-escalation-record.schema.json -d "$TMP_FILE"; then
  rm -f "$TMP_FILE"
  exit 0
else
  rm -f "$TMP_FILE"
  exit 1
fi
