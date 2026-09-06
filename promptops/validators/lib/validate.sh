#!/usr/bin/env bash
set -e

validator_dir="$(cd "$(dirname "$0")" && pwd)"
schema_name="$1"
shift
format_args=()
if [ "${1:-}" = "--formats" ]; then
  format_args=(-c ajv-formats)
  shift
fi
if [ "$#" -ne 1 ]; then
  echo "Usage: validate-$schema_name.sh <file.json|yaml>" >&2
  exit 1
fi
if [ ! -f "$1" ]; then
  echo "File not found: $1" >&2
  exit 1
fi

schema_file="$validator_dir/../../schemas/$schema_name.schema.json"
schema_draft="$(node -e 'const schema = require(process.argv[1]); process.stdout.write(schema.$schema.includes("2020-12") ? "draft2020" : "draft7")' "$schema_file")"
reference_args=()
if [ "$schema_name" = "quick-eval" ]; then
  reference_args=(-r "$validator_dir/../../schemas/dataset-case.schema.json")
elif [ "$schema_name" = "prompt-package" ]; then
  reference_args=(-r "$validator_dir/../../schemas/prompt-spec.schema.json")
fi
. "$validator_dir/ajv.sh"
apastra_ajv_validate "$schema_file" "$1" --spec="$schema_draft" --strict=false --all-errors "${format_args[@]}" "${reference_args[@]}"
