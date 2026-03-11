#### 1. Context & Goal
- **Objective**: Implement validation of consumption manifests against the CONTRACTS schema.
- **Trigger**: The `.jules/RUNTIME.md` indicates that the consumption manifest format task was previously blocked waiting for the `consumption-manifest.schema.json` dependency from CONTRACTS.
- **Impact**: Ensures that invalid manifests fail fast, enforcing the schema contract for all downstream consumers.

#### 2. File Inventory
- **Create**: None
- **Modify**: `promptops/runtime/resolve.py`
- **Read-Only**: `promptops/schemas/consumption-manifest.schema.json`

#### 3. Implementation Spec
- **Resolver Architecture**: When loading a manifest in `load_manifest`, before returning the wrapper, validate the manifest data against `consumption-manifest.schema.json`. The python runtime should invoke `npx ajv-cli validate -s promptops/schemas/consumption-manifest.schema.json -d <temp_json_file> --spec=draft2020 --strict=false` via a subprocess call. The manifest content will need to be dumped to a temporary JSON file to satisfy ajv-cli. If validation fails, raise a `RuntimeError` detailing the schema violations.
- **Manifest Format**: Unchanged.
- **Pseudo-Code**:
  1. In `load_manifest`, if `data` is a dictionary:
  2. Dump `data` to a temporary `.json` file using `json.dump`.
  3. Run `npx ajv-cli validate -s promptops/schemas/consumption-manifest.schema.json -d <temp_file.json> --spec=draft2020 --strict=false` via `subprocess.run()`.
  4. If return code is not 0, parse stdout/stderr and raise `RuntimeError("Manifest schema validation failed: " + details)`.
  5. Delete the temporary file.
- **Harness Contract Interface**: Not applicable.
- **Dependencies**: CONTRACTS `promptops/schemas/consumption-manifest.schema.json`

#### 4. Test Plan
- **Verification**: `mkdir -p test-fixtures && echo 'prompts: {}' > test-fixtures/invalid-manifest.yaml && python -c "import sys; from promptops.runtime.resolve import load_manifest; load_manifest('test-fixtures/invalid-manifest.yaml')" 2>/dev/null`
- **Success Criteria**: `[ $? -ne 0 ]`
- **Edge Cases**: `mkdir -p test-fixtures && echo '{"version": "1", "prompts": {"my-prompt": {"pin": "sha256:123"}}}' > test-fixtures/valid-manifest.json && python -c "from promptops.runtime.resolve import load_manifest; load_manifest('test-fixtures/valid-manifest.json')" && [ $? -eq 0 ]`
