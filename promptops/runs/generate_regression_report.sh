#!/bin/bash
set -eo pipefail

if [ "$#" -ne 4 ]; then
    echo "Usage: $0 <candidate_scorecard> <baseline_scorecard> <policy_file> <report_id>"
    exit 1
fi

CANDIDATE="$1"
BASELINE="$2"
POLICY="$3"
REPORT_ID="$4"

if [ ! -f "$CANDIDATE" ]; then
    echo "Error: Candidate scorecard not found: $CANDIDATE"
    exit 1
fi

if [ ! -f "$BASELINE" ]; then
    echo "Error: Baseline scorecard not found: $BASELINE"
    exit 1
fi

if [ ! -f "$POLICY" ]; then
    echo "Error: Policy file not found: $POLICY"
    exit 1
fi

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TEMP_REPORT=$(mktemp --suffix=.json)
trap 'rm -f "$TEMP_REPORT"' EXIT

echo "Generating regression report..."
python "$SCRIPT_DIR/compare.py" "$CANDIDATE" "$BASELINE" "$POLICY" "$TEMP_REPORT"

echo "Validating regression report..."
npx --yes ajv-cli validate -s "$SCRIPT_DIR/../schemas/regression-report.schema.json" -d "$TEMP_REPORT" --spec=draft2020 --strict=false -c ajv-formats >/dev/null

mkdir -p "derived-index/regressions"
REPORT_PATH="derived-index/regressions/${REPORT_ID}.json"

mv "$TEMP_REPORT" "$REPORT_PATH"
echo "Regression report written to $REPORT_PATH"
