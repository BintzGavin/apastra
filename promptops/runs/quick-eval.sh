#!/bin/bash
set -e

if [ -z "$1" ]; then
    echo "Usage: $0 <quick-eval.yaml>"
    return 1 2>/dev/null
fi

EVAL_FILE="$1"
RUN_ID=$(basename "$EVAL_FILE" .yaml)-$(date +%s)
TMP_DIR=$(mktemp -d)
OUTPUT_DIR="promptops/runs/$RUN_ID"

# Use python to parse yaml and create standard request files
python3 -c "
import sys, yaml, json, os, hashlib

def sha256(content):
    return 'sha256:' + hashlib.sha256(content.encode('utf-8')).hexdigest()

with open('$EVAL_FILE', 'r') as f:
    data = yaml.safe_load(f)

cases_path = os.path.join('$TMP_DIR', 'cases.jsonl')
cases_content = ''
with open(cases_path, 'w') as f:
    for case in data.get('cases', []):
        case_json = json.dumps(case) + '\\n'
        f.write(case_json)
        cases_content += case_json

prompt_template = data.get('prompt', '')

request = {
    'suite_id': data.get('id', 'quick-eval'),
    'revision_ref': 'quick-eval-mode',
    'model_matrix': ['mock-model'],
    'evaluator_refs': ['inline-asserts'],
    'dataset_path': cases_path,
    'prompt_template': prompt_template,
    'prompt_digest': sha256(prompt_template),
    'dataset_digest': sha256(cases_content),
    'evaluator_digest': sha256('inline-asserts'),
    'harness_version': '1.0.0'
}

request_path = os.path.join('$TMP_DIR', 'run_request.json')
with open(request_path, 'w') as f:
    json.dump(request, f)
"

# Run reference adapter
python3 promptops/harnesses/reference-adapter/run.py "$TMP_DIR/run_request.json" "$OUTPUT_DIR"

# Clean up
rm -rf "$TMP_DIR"
echo "Quick eval complete. Artifacts in $OUTPUT_DIR"
