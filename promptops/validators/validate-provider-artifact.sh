#!/bin/bash
set -e

if [ -z "$1" ]; then
  echo "Usage: $0 <provider-artifact.json>"
  exit 1
fi

FILE="$1"
TEMP_FILE=""

if [[ "$FILE" == *.yaml || "$FILE" == *.yml ]]; then
  TEMP_FILE="$(mktemp --suffix=.json)"
  yq . "$FILE" > "$TEMP_FILE"
  FILE="$TEMP_FILE"
fi

npx --yes ajv-cli validate -s promptops/schemas/provider-artifact.schema.json -d "$FILE" --spec=draft2020 --strict=false -c ajv-formats

if [ -n "$TEMP_FILE" ]; then
  rm -f "$TEMP_FILE"
fi