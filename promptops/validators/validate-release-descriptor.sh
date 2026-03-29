#!/bin/bash
set -e

SCHEMA="promptops/schemas/release-descriptor.schema.json"

if [ -z "$1" ]; then
  echo "Usage: $0 <release-descriptor-json>"
  exit 1
fi

TARGET="$1"

if ! command -v ajv &> /dev/null; then
    echo "ajv could not be found. Please install it with 'npm install -g ajv-cli ajv-formats'."
    exit 1
fi

ajv validate -c ajv-formats -s "$SCHEMA" -d "$TARGET" --all-errors