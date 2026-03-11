#!/bin/bash
set -e

if [ "$#" -ne 3 ]; then
  echo "Usage: $0 <suite_id> <name> <run_artifact_digest>"
  exit 1
fi

SUITE_ID=$1
NAME=$2
RUN_DIGEST=$3

# Basic digest validation (must start with sha256:)
if [[ ! "$RUN_DIGEST" == sha256:* ]]; then
  echo "Error: run_artifact_digest must start with sha256:"
  exit 1
fi

BASELINE_ID="${SUITE_ID}-${NAME}"
CREATED_AT=$(date -u +"%Y-%m-%dT%H:%M:%SZ")

mkdir -p derived-index/baselines/

TEMP_JSON=$(mktemp --suffix=.json)
cat <<JSON > "$TEMP_JSON"
{
  "baseline_id": "${BASELINE_ID}",
  "run_digest": "${RUN_DIGEST}",
  "created_at": "${CREATED_AT}",
  "description": "Established baseline for ${SUITE_ID}"
}
JSON

if ! npx --yes ajv-cli validate -s promptops/schemas/baseline.schema.json -d "$TEMP_JSON" --spec=draft2020 --strict=false -c ajv-formats; then
    echo "Validation failed against baseline.schema.json"
    rm -f "$TEMP_JSON"
    exit 1
fi

BASELINE_FILE="derived-index/baselines/${BASELINE_ID}.json"

if [ -f "$BASELINE_FILE" ]; then
    echo "Error: Baseline ${BASELINE_ID} already exists."
    rm -f "$TEMP_JSON"
    exit 1
fi

cp "$TEMP_JSON" "$BASELINE_FILE"
rm -f "$TEMP_JSON"

echo "Baseline successfully established at $BASELINE_FILE"
