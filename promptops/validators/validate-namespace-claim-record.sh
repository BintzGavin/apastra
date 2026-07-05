#!/usr/bin/env bash
set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
. "$SCRIPT_DIR/lib/ajv.sh"

if [ "$#" -ne 1 ]; then
    echo "Usage: $0 <namespace_claim_record_file.json_or_yaml>"
    exit 1
fi

if [ ! -f "$1" ]; then
    echo "Error: File '$1' not found."
    exit 1
fi

apastra_ajv_validate promptops/schemas/namespace-claim-record.schema.json "$1" --spec=draft2020 --strict=false -c ajv-formats
