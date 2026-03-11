#!/bin/bash
if [ "$#" -ne 2 ]; then
    echo "Usage: $0 <staging_dir> <output_dir>"
    exit 1
fi

STAGING_DIR="$1"
OUTPUT_DIR="$2"
RUN_ARTIFACT="$STAGING_DIR/run_artifact.json"

if [ ! -f "$RUN_ARTIFACT" ]; then
    echo "Error: $RUN_ARTIFACT not found"
    exit 1
fi

mkdir -p "$OUTPUT_DIR"

jq '.manifest' "$RUN_ARTIFACT" > "$OUTPUT_DIR/run_manifest.json"
jq '.scorecard' "$RUN_ARTIFACT" > "$OUTPUT_DIR/scorecard.json"
jq -c '.cases[]' "$RUN_ARTIFACT" > "$OUTPUT_DIR/cases.jsonl"
jq '.failures' "$RUN_ARTIFACT" > "$OUTPUT_DIR/failures.json"

# Generate dummy digest and artifact refs for now
echo '{"references":{}}' > "$OUTPUT_DIR/artifact_refs.json"

echo "Artifact split complete in $OUTPUT_DIR"
