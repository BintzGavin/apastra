#!/usr/bin/env bash
set -e
if [ -z "$1" ]; then
  echo "Usage: $0 <ownership-dispute-record.json|yaml>"
  exit 1
fi

if [[ "$1" == *.yaml ]] || [[ "$1" == *.yml ]]; then
  # Convert YAML to JSON, then validate
  python3 -c 'import sys, yaml, json; json.dump(yaml.safe_load(sys.stdin), sys.stdout)' < "$1" | ajv validate -c ajv-formats -s promptops/schemas/ownership-dispute-record.schema.json -d -
else
  ajv validate -c ajv-formats -s promptops/schemas/ownership-dispute-record.schema.json -d "$1"
fi