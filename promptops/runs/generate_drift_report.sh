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
    echo "Error: candidate scorecard '$CANDIDATE' not found."
    exit 1
fi

if [ ! -f "$BASELINE" ]; then
    echo "Error: baseline scorecard '$BASELINE' not found."
    exit 1
fi

if [ ! -f "$POLICY" ]; then
    echo "Error: policy file '$POLICY' not found."
    exit 1
fi

TMP_REPORT=$(mktemp)
python3 promptops/runs/compare.py "$CANDIDATE" "$BASELINE" "$POLICY" "$TMP_REPORT"

# Format to drift report schema
python3 -c "
import json
import sys

try:
    with open('$TMP_REPORT', 'r') as f:
        report = json.load(f)

    drift_detected = report.get('status') in ['fail', 'warning']
    evidence = []
    for e in report.get('evidence', []):
        ev = {
            'metric_name': e.get('metric'),
            'baseline_value': e.get('baseline_value'),
            'current_value': e.get('candidate_value')
        }
        if 'delta' in e and e['delta'] is not None:
            ev['delta'] = e['delta']
        evidence.append(ev)

    drift_report = {
        'baseline_ref': report.get('baseline_ref'),
        'current_ref': report.get('candidate_ref'),
        'drift_detected': drift_detected,
        'evidence': evidence
    }
    with open('$TMP_REPORT', 'w') as f:
        json.dump(drift_report, f, indent=2)

except Exception as e:
    print(f'Error formatting report: {e}')
    sys.exit(1)
"

npx ajv-cli validate -s promptops/schemas/drift-report.schema.json -d "$TMP_REPORT"

mkdir -p derived-index/regressions
OUTPUT_PATH="derived-index/regressions/${REPORT_ID}.json"

mv "$TMP_REPORT" "$OUTPUT_PATH"
echo "Drift report generated and validated at $OUTPUT_PATH"
