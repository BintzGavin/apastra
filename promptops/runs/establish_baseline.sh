#!/usr/bin/env bash
set -euo pipefail
if [ "$#" -ne 4 ]; then
  echo "Usage: $0 <suite_id> <name> <run_directory> <approved_adapter>" >&2
  exit 1
fi
script_dir="$(cd "$(dirname "$0")" && pwd)"
exec "${PYTHON:-python3}" "$script_dir/../runtime/cli.py" baseline "$1" "$2" "$3" --adapter "$4"
