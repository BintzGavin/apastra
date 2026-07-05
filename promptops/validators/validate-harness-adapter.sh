#!/bin/bash

# Validator script for harness adapter specs
set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
. "$SCRIPT_DIR/lib/ajv.sh"

if [ -z "$1" ]; then
  echo "Usage: $0 <harness-adapter-spec-file>"
  exit 1
fi

TARGET_FILE="$1"

if [ ! -f "$TARGET_FILE" ]; then
  echo "Error: File '$TARGET_FILE' not found."
  exit 1
fi

apastra_ajv_validate promptops/schemas/harness-adapter.schema.json "$TARGET_FILE" --spec=draft2020 --strict=false
