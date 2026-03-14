#!/bin/bash
set -e

if [ -z "$1" ]; then
    echo "Usage: $0 <quick-eval.yaml>"
    return 1 2>/dev/null || true
fi

EVAL_FILE="$1"
RUN_ID=$(basename "$EVAL_FILE" .yaml)-$(date +%s)
TMP_DIR=$(mktemp -d)
OUTPUT_DIR="promptops/runs/$RUN_ID"

# Use python to parse yaml and create standard request files
python3 -c "
import sys, yaml, json, os

eval_file = sys.argv[1]
tmp_dir = sys.argv[2]

with open(eval_file, 'r') as f:
    data = yaml.safe_load(f)

cases_path = os.path.join(tmp_dir, 'cases.jsonl')
with open(cases_path, 'w') as f:
    for case in data.get('cases', []):
        f.write(json.dumps(case) + '\n')

request = {
    'suite_id': data.get('id', 'quick-eval'),
    'revision_ref': 'quick-eval-mode',
    'model_matrix': ['mock-model'],
    'evaluator_refs': ['inline-asserts'],
    'dataset_path': cases_path,
    'prompt_template': data.get('prompt', '')
}

request_path = os.path.join(tmp_dir, 'run_request.json')
with open(request_path, 'w') as f:
    json.dump(request, f)
" "$EVAL_FILE" "$TMP_DIR"

# Run reference adapter
python3 promptops/harnesses/reference-adapter/run.py "$TMP_DIR/run_request.json" "$OUTPUT_DIR"

# Clean up
rm -rf "$TMP_DIR"
echo "Quick eval complete. Artifacts in $OUTPUT_DIR"
