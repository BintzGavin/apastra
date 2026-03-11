#### 1. Context & Goal
- **Objective**: Create a JSON Schema and validation script for `harness-adapter`.
- **Trigger**: `README.md` requires harness adapters to integrate and execute benchmark suites to produce run artifacts. The `EVALUATION` domain is currently blocked waiting for this schema.
- **Impact**: Unblocks the `EVALUATION` domain to implement the harness adapter contract definition and runner.

#### 2. File Inventory
- **Create**:
  - `promptops/schemas/harness-adapter.schema.json` (The JSON Schema definition)
  - `promptops/validators/validate-harness-adapter.sh` (The validation script)
- **Modify**: None.
- **Read-Only**: `README.md`, `promptops/schemas/digest-convention.md`

#### 3. Implementation Spec
- **Schema Architecture**:
  - Format: JSON Schema (draft 2020-12)
  - Required fields:
    - `id`: string (stable identifier for the harness adapter)
    - `type`: string (must be "harness_adapter")
    - `capabilities`: array of strings (e.g., ["run_suite", "trials", "model_matrix"])
    - `entrypoint`: string (e.g., the CLI command or script to invoke the harness)
  - Optional fields:
    - `description`: string
    - `env_vars`: array of strings (required environment variables, e.g., "OPENAI_API_KEY")
    - `digest`: string (content digest stored inline)
  - Validation rules: `id` and `type` must match specific patterns. `capabilities` should contain valid enum values if possible or be a string array.
- **Content Digest Convention**:
  - Computed via `SHA-256` of canonical JSON.
  - For YAML files, use `yq .` to convert to JSON, then canonicalize using `jq -cSM .` before hashing.
  - Stored in the `digest` field.
- **Pseudo-Code**:
  - Load the test fixture JSON or YAML.
  - If YAML, convert to JSON.
  - Validate the JSON against `harness-adapter.schema.json` using `ajv-cli`.
- **Public Contract Changes**:
  - Exports schema ID `https://apastra.com/schemas/harness-adapter.schema.json`.
- **Dependencies**:
  - None.

#### 4. Test Plan
- **Verification**:
  - `npx ajv-cli validate -s promptops/schemas/harness-adapter.schema.json -d test-fixtures/valid-harness-adapter.json --spec=draft2020 --strict=false`
  - `./promptops/validators/validate-harness-adapter.sh test-fixtures/valid-harness-adapter.json`
- **Success Criteria**:
  - `ajv-cli` outputs `test-fixtures/valid-harness-adapter.json valid`.
  - The bash script returns exit code 0.
- **Edge Cases**:
  - Missing required fields (e.g., `id`, `type`, `capabilities`) should be rejected.
  - Incorrect types for `entrypoint` should be rejected.