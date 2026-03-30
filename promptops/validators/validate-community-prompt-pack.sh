#!/bin/bash
set -e

if [ "$#" -ne 1 ]; then
    echo "Usage: $0 <community-prompt-pack.json>"
    exit 1
fi

FILE=$1
SCHEMA_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../schemas" && pwd)"
SCHEMA_FILE="$SCHEMA_DIR/community-prompt-pack.schema.json"

if ! command -v ajv &> /dev/null; then
    echo "Error: ajv is required but not installed. Run 'npm install -g ajv-cli' to install it."
    exit 1
fi

ajv validate --spec=draft2020 -s "$SCHEMA_FILE" -d "$FILE"
