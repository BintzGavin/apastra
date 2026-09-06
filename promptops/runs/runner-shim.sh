#!/usr/bin/env bash
set -euo pipefail

if [ "$#" -ne 3 ]; then
  echo "Usage: $0 <adapter> <run_request.json> <output_dir>" >&2
  exit 1
fi
script_dir="$(cd "$(dirname "$0")" && pwd)"
exec "${PYTHON:-python3}" "$script_dir/../runtime/runner.py" "$2" "$1" "$3"
