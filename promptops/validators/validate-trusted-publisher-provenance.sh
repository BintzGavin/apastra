#!/bin/bash
set -e
if [ -z "$1" ]; then
  echo "Usage: $0 <record.json>"
  exit 1
fi
ajv validate -c ajv-formats -s promptops/schemas/trusted-publisher-provenance.schema.json -d "$1"
