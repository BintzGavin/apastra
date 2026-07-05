#!/bin/bash
set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
. "$SCRIPT_DIR/lib/ajv.sh"

INPUT_FILE="$1"

if [ -z "$INPUT_FILE" ]; then
  echo "Usage: $0 <emergency-takedown-decision.json|yaml>"
  exit 1
fi

if [ ! -f "$INPUT_FILE" ]; then
  echo "File not found: $INPUT_FILE"
  exit 1
fi

apastra_ajv_validate promptops/schemas/emergency-takedown-decision.schema.json "$INPUT_FILE" --spec=draft2020 --strict=false -c ajv-formats
