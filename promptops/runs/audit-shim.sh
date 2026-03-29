#!/bin/bash
set -eo pipefail
if [ "$#" -ne 1 ]; then
    echo "Usage: $0 <output_dir>"
    exit 1
fi
OUTPUT_DIR="$1"
mkdir -p "$OUTPUT_DIR"
REPORT_PATH="$OUTPUT_DIR/audit_report.json"
python3 -c "
import sys, os, json, datetime
sys.path.insert(0, os.path.abspath('.'))
try:
    from promptops.runtime.audit import scan_codebase
except ImportError:
    print('Failed to import promptops.runtime.audit')
    sys.exit(1)
report = scan_codebase('.')
formatted_report = {
    'timestamp': datetime.datetime.utcnow().isoformat() + 'Z',
    'scanned_paths': ['.'],
    'total_prompts': report.get('detected_prompts', 0),
    'untested_prompts': report.get('detected_prompts', 0),
    'unversioned_prompts': report.get('detected_prompts', 0),
    'severity_score': report.get('debt_score', 0),
    'findings': []
}
for finding in report.get('findings', []):
    formatted_report['findings'].append({
        'file_path': finding.get('file', ''),
        'issue_type': 'hardcoded_prompt',
        'suggestion': 'Extract hardcoded prompt into a versioned spec file in promptops/prompts/'
    })
with open(sys.argv[1], 'w') as f:
    json.dump(formatted_report, f, indent=2)
" "$REPORT_PATH"
echo "Audit scan complete. Generating report..."
npx --yes ajv-cli validate -s promptops/schemas/audit-report.schema.json -d "$REPORT_PATH" --spec=draft2020 --strict=false -c ajv-formats
echo "Audit report generated and validated at $REPORT_PATH"