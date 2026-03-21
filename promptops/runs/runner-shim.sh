#!/bin/bash

# promptops/runs/runner-shim.sh
# Usage: ./runner-shim.sh <adapter_yaml> <run_request> <output_dir>

set -eo pipefail

if [ "$#" -ne 3 ]; then
    echo "Usage: $0 <adapter_yaml> <run_request> <output_dir>"
    exit 1
fi

ADAPTER_YAML="$1"
RUN_REQUEST="$2"
OUTPUT_DIR="$3"

if [ ! -f "$ADAPTER_YAML" ]; then
    echo "Error: adapter YAML '$ADAPTER_YAML' not found."
    exit 1
fi

if [ ! -f "$RUN_REQUEST" ]; then
    echo "Error: run request JSON '$RUN_REQUEST' not found."
    exit 1
fi

# Ensure output directory exists
mkdir -p "$OUTPUT_DIR"

# Parse entrypoint from adapter YAML
ENTRYPOINT=$(python3 -c "import sys, yaml; print(yaml.safe_load(sys.stdin).get('entrypoint', ''))" < "$ADAPTER_YAML")

if [ -z "$ENTRYPOINT" ]; then
    echo "Error: 'entrypoint' not found or empty in $ADAPTER_YAML"
    exit 1
fi

echo "Running adapter via entrypoint: $ENTRYPOINT"

# Execute the entrypoint with arguments
$ENTRYPOINT "$RUN_REQUEST" "$OUTPUT_DIR"

# Basic verification: check if run_manifest.json exists in the output directory
if [ ! -f "$OUTPUT_DIR/run_manifest.json" ]; then
    echo "Warning: run_manifest.json not found in output directory ($OUTPUT_DIR). The adapter may not have completed successfully or may be non-compliant."
else
    echo "Adapter run complete. Artifacts collected in $OUTPUT_DIR."
fi

# Return the path to the collected artifacts
echo "$OUTPUT_DIR"
