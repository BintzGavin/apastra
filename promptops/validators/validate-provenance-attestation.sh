#!/bin/bash
set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
. "$SCRIPT_DIR/lib/ajv.sh"

if [ -z "$1" ]; then
    echo "Usage: $0 <provenance-attestation.json|yaml>"
    exit 1
fi

INPUT_FILE="$1"

if [ ! -f "$INPUT_FILE" ]; then
    echo "File not found: $INPUT_FILE"
    exit 1
fi

apastra_ajv_validate promptops/schemas/provenance-attestation.schema.json "$INPUT_FILE" --spec=draft2020 --strict=false -c ajv-formats
