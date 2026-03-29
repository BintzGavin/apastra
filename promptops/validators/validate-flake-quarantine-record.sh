#!/bin/bash
set -e

if [ "$#" -ne 1 ]; then
    echo "Usage: $0 <path-to-flake-quarantine-record.json>"
    exit 1
fi

FILE=$1
SCHEMA="$(dirname "$0")/../schemas/flake-quarantine-record.schema.json"

if [ ! -f "$FILE" ]; then
    echo "Error: File '$FILE' not found."
    exit 1
fi

if ! command -v ajv &> /dev/null; then
    echo "Error: ajv-cli is not installed. Please install it using 'npm install -g ajv-cli ajv-formats'."
    exit 1
fi

ajv validate -c ajv-formats -s "$SCHEMA" -d "$FILE" --all-errors