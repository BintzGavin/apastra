#!/bin/bash
set -e

OUTPUT_DIR="${1:-.}"
TARGET_DIR="."
OUTPUT_FILE="$OUTPUT_DIR/audit_report.json"
TIMESTAMP=$(date -u +"%Y-%m-%dT%H:%M:%SZ")

echo "Scanning $TARGET_DIR for hardcoded prompts..."

FINDINGS_FILE=$(mktemp)

grep -rnEwi "prompt|system prompt|you are a helpful assistant" "$TARGET_DIR" \
    --exclude-dir={.git,node_modules,venv,__pycache__,derived-index,promptops} \
    --exclude="*.json" \
    --exclude="*.md" \
    --exclude="*.yaml" \
    --exclude="*.yml" \
    --exclude="audit-shim.sh" > "$FINDINGS_FILE" || true

TOTAL_PROMPTS=$(wc -l < "$FINDINGS_FILE" | tr -d ' ')

UNTESTED_PROMPTS=$TOTAL_PROMPTS
UNVERSIONED_PROMPTS=$TOTAL_PROMPTS

if [ "$TOTAL_PROMPTS" -gt 10 ]; then
    SEVERITY=3
elif [ "$TOTAL_PROMPTS" -gt 0 ]; then
    SEVERITY=2
else
    SEVERITY=1
fi

FINDINGS_JSON="["
FIRST=1
while IFS= read -r line; do
    if [ -z "$line" ]; then continue; fi
    FILE_PATH=$(echo "$line" | cut -d: -f1)

    if [ $FIRST -eq 0 ]; then
        FINDINGS_JSON="${FINDINGS_JSON},"
    fi
    FIRST=0

    FINDINGS_JSON="${FINDINGS_JSON}{\"file_path\": \"$FILE_PATH\", \"issue_type\": \"hardcoded_prompt\", \"suggestion\": \"Extract to promptops manifest\"}"
done < <(head -n 50 "$FINDINGS_FILE")
FINDINGS_JSON="${FINDINGS_JSON}]"

cat << INNEREOF > "$OUTPUT_FILE"
{
  "timestamp": "$TIMESTAMP",
  "scanned_paths": ["$TARGET_DIR"],
  "total_prompts": $TOTAL_PROMPTS,
  "untested_prompts": $UNTESTED_PROMPTS,
  "unversioned_prompts": $UNVERSIONED_PROMPTS,
  "severity_score": $SEVERITY,
  "findings": $FINDINGS_JSON
}
INNEREOF

echo "Audit report generated at $OUTPUT_FILE"
rm "$FINDINGS_FILE"

ajv validate --spec=draft2020 -c ajv-formats -s promptops/schemas/audit-report.schema.json -d "$OUTPUT_FILE"
