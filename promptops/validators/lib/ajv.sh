#!/usr/bin/env bash

apastra_ajv_validate() {
  local schema_file="$1"
  local data_file="$2"
  shift 2

  # Resolve installed dependencies from the schema's package, not the caller's
  # working directory. Validation must never install tools or contact npm.
  local ajv_entrypoint=""
  local ajv_command=()
  if ajv_entrypoint="$(node -e '
const path = require("path");
try {
  process.stdout.write(require.resolve("ajv-cli/dist/index.js", {
    paths: [path.dirname(path.resolve(process.argv[1]))]
  }));
} catch {
  process.exit(1);
}
' "$schema_file" 2>/dev/null)"; then
    ajv_command=(node "$ajv_entrypoint")
  elif command -v ajv >/dev/null 2>&1; then
    ajv_entrypoint="$(command -v ajv)"
    ajv_command=(ajv)
  else
    echo "Error: AJV is not installed. Install Apastra's npm dependencies or provide ajv-cli on the executable search path." >&2
    return 1
  fi

  local tmp_dir
  tmp_dir="$(mktemp -d "/tmp/apastra-ajv.XXXXXX")"
  local target_file="$tmp_dir/data.json"
  if ! node - "$schema_file" "$data_file" "$target_file" "$ajv_entrypoint" <<'JS'
const fs = require("fs");
const path = require("path");
const [schema, source, target, entrypoint] = process.argv.slice(2);
try {
  const search = [path.dirname(path.resolve(schema)), path.dirname(fs.realpathSync(entrypoint))];
  const yaml = require(require.resolve("js-yaml", { paths: search }));
  const sourceText = fs.readFileSync(source, "utf8");
  if (source.endsWith(".json")) JSON.parse(sourceText); // Strict JSON syntax.
  // YAML's parser also rejects duplicate keys in JSON objects.
  const data = yaml.load(sourceText, { schema: yaml.CORE_SCHEMA });
  const active = new Set();
  function validate(value) {
    if (typeof value === "number" && !Number.isFinite(value)) throw new Error("Nonfinite value");
    if (value === undefined) throw new Error("Empty document");
    if (value && typeof value === "object") {
      if (active.has(value)) throw new Error("Cyclic data");
      active.add(value);
      for (const child of Object.values(value)) validate(child);
      active.delete(value);
    }
  }
  validate(data);
  fs.writeFileSync(target, JSON.stringify(data));
} catch {
  process.stderr.write("Invalid asset: malformed data, duplicate keys, nonfinite values, or unavailable parser.\\n");
  process.exit(1);
}
JS
  then
    rm -r -- "$tmp_dir"
    return 1
  fi
  local status=0
  "${ajv_command[@]}" validate -s "$schema_file" -d "$target_file" "$@" || status=$?
  rm -r -- "$tmp_dir"
  return "$status"
}
