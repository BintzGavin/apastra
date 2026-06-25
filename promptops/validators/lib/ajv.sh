#!/usr/bin/env bash

apastra_ajv_validate() {
  local schema_file="$1"
  local data_file="$2"
  shift 2

  local target_file="$data_file"
  local tmp_dir=""
  local tmp_file=""

  case "$data_file" in
    *.yaml|*.yml)
      tmp_dir="$(mktemp -d "${TMPDIR:-/tmp}/apastra-ajv.XXXXXX")"
      tmp_file="$tmp_dir/data.json"
      if command -v node >/dev/null 2>&1 && node -e 'require("js-yaml")' >/dev/null 2>&1; then
        if ! node - "$data_file" "$tmp_file" <<'JS'
const fs = require("fs");
const yaml = require("js-yaml");

const source = process.argv[2];
const target = process.argv[3];
const data = yaml.load(fs.readFileSync(source, "utf8"));
fs.writeFileSync(target, JSON.stringify(data));
JS
        then
          rm -rf "$tmp_dir"
          return 1
        fi
      elif command -v ruby >/dev/null 2>&1; then
        if ! ruby -ryaml -rjson -e 'data = YAML.safe_load(File.read(ARGV[0]), permitted_classes: [], permitted_symbols: [], aliases: true); File.write(ARGV[1], JSON.generate(data))' "$data_file" "$tmp_file"; then
          rm -rf "$tmp_dir"
          return 1
        fi
      elif python3 -c 'import yaml' >/dev/null 2>&1; then
        if ! python3 - "$data_file" "$tmp_file" <<'PY'
import json
import sys
from pathlib import Path

import yaml

source = Path(sys.argv[1])
target = Path(sys.argv[2])
with source.open("r", encoding="utf-8") as handle:
    data = yaml.safe_load(handle)
with target.open("w", encoding="utf-8") as handle:
    json.dump(data, handle, separators=(",", ":"))
PY
        then
          rm -rf "$tmp_dir"
          return 1
        fi
      else
        echo "Error: YAML validation requires one YAML parser: node with js-yaml, ruby, or python with pyyaml." >&2
        echo "Install pyyaml manually, or rerun Apastra setup with APASTRA_INSTALL_PY_DEPS=1." >&2
        rm -rf "$tmp_dir"
        return 1
      fi
      target_file="$tmp_file"
      ;;
  esac

  npx ajv-cli validate -s "$schema_file" -d "$target_file" "$@"
  local status=$?
  rm -rf "$tmp_dir"
  return "$status"
}
