#!/usr/bin/env bash
set -euo pipefail
if [ "$#" -ne 5 ]; then
  echo "Usage: $0 <candidate_run> <baseline_run> <policy> <report_id> <approved_adapter>" >&2
  exit 1
fi
if [[ ! "$4" =~ ^[a-zA-Z0-9][a-zA-Z0-9._-]*$ ]]; then
  echo "Unsafe report ID" >&2
  exit 1
fi
script_dir="$(cd "$(dirname "$0")" && pwd)"
exec "${PYTHON:-python3}" "$script_dir/compare.py" "$1" "$2" "$3" "derived-index/regressions/$4.json" --adapter "$5"
