#### 1. Context & Goal
- **Objective**: Define the foundational machine-readable schema for prompt specifications.
- **Trigger**: `README.md` requires "Prompt spec: Source-of-truth prompt definition with a stable ID, variable schema, output contract, and metadata." Currently, `promptops/schemas/` is missing this core contract.
- **Impact**: Unlocks RUNTIME's ability to render templates and EVALUATION's ability to read prompt configurations for suites. All prompt instances and run requests depend on this schema existing first.

#### 2. File Inventory
- **Create**:
  - `promptops/schemas/prompt-spec.schema.json` - JSON Schema defining the structure of a prompt spec (ID, vars, output contract, metadata).
  - `promptops/validators/validate-prompt-spec.sh` - Simple CLI tool to validate a YAML/JSON prompt spec against the schema.
- **Modify**: None.
- **Read-Only**: `README.md` (for noun definitions).

#### 3. Implementation Spec
- **Schema Architecture**:
  - Format: JSON Schema (Draft 2020-12).
  - Required fields:
    - `id` (string): Stable identifier for the prompt (e.g., `my-app/summarize-v1`).
    - `variables` (object): Map of variable names to their JSON Schema types (e.g., `{"text": {"type": "string"}}`).
    - `template` (string or object): The prompt template content (e.g., Jinja2 string, or array of message objects for chat models).
  - Optional fields:
    - `output_contract` (object): JSON Schema defining the expected output structure from the model.
    - `metadata` (object): Arbitrary key-value pairs (e.g., author, intent, tags).
- **Content Digest Convention**:
  - Prompt specs themselves do not hold their own content digest in the schema; the digest is computed by the registry/packager across the canonicalized JSON of the file.
- **Pseudo-Code** (Validator):
  ```bash
  # promptops/validators/validate-prompt-spec.sh
  # 1. Take input file path (YAML or JSON)
  # 2. Convert YAML to JSON (if needed)
  # 3. Run ajv-cli (or similar) against promptops/schemas/prompt-spec.schema.json
  # 4. Exit 0 on success, exit 1 on failure
  ```
- **Public Contract Changes**:
  - Exports new schema ID: `https://promptops.apastra.com/schemas/prompt-spec.schema.json`
- **Dependencies**: None. This is the foundational first step.

#### 4. Test Plan
- **Verification**: `npx ajv-cli validate -s promptops/schemas/prompt-spec.schema.json -d test-fixtures/valid-prompt-spec.json`
- **Success Criteria**: Validator exits with code 0 and outputs "valid-prompt-spec.json is valid".
- **Edge Cases**:
  - Reject prompt specs missing the `id`, `variables`, or `template` fields.
  - Reject specs where `variables` is not an object.
