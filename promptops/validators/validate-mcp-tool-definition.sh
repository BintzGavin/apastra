#!/bin/bash

# Validator script for MCP tool definitions

SCHEMA_PATH="promptops/schemas/mcp-tool-definition.schema.json"

if [ -z "$1" ]; then
  echo "Usage: $0 <mcp-tool-definition-file>"
  exit 1
fi

TARGET_FILE="$1"

if [ ! -f "$TARGET_FILE" ]; then
  echo "Error: Target file '$TARGET_FILE' not found."
  exit 1
fi

echo "Validating $TARGET_FILE against $SCHEMA_PATH..."
ajv validate -s "$SCHEMA_PATH" -d "$TARGET_FILE"
