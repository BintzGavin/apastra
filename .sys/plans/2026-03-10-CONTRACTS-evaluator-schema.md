#### 1. Context & Goal
- **Objective**: Create the JSON Schema and a bash validator script for Evaluator specs.
- **Trigger**: The `README.md` defines an evaluator as a "Scoring definition (deterministic checks, schema validation, rubric/judge config)". The schemas for prompt specs and datasets exist, making evaluator the next foundational gap to close.
- **Impact**: Unlocks the ability for RUNTIME and EVALUATION domains to build suite configurations and run requests, as suites depend on evaluators.

#### 2. File Inventory
- **Create**:
  - `promptops/schemas/evaluator.schema.json`: JSON Schema defining the structure of an evaluator.
  - `promptops/validators/validate-evaluator.sh`: Bash script to validate evaluator specs against the schema using `ajv-cli`.
- **Modify**: None.
- **Read-Only**: `README.md`, `promptops/schemas/prompt-spec.schema.json`.

#### 3. Implementation Spec
- **Schema Architecture**:
  - The evaluator schema will be a JSON Schema supporting JSON and YAML files.
  - Required fields: `id` (string), `type` (enum: `deterministic`, `schema`, `judge`), `metrics` (array of strings, e.g., `["exact_match"]` or `["helpfulness"]`).
  - Optional fields: `description` (string), `config` (object containing judge config like `model` and `prompt_ref`, or deterministic config like `target_value`).
- **Content Digest Convention**:
  - A `digest` property is NOT strictly required inside the schema definition itself as it's typically computed externally during packaging, but if present, it should be a SHA-256 hash.
- **Pseudo-Code**:
  - The validation flow in `validate-evaluator.sh` will run `npx ajv-cli validate -s promptops/schemas/evaluator.schema.json -d "$1" --spec=draft2020 --strict=false`.
- **Public Contract Changes**:
  - Exports a new schema for evaluator configurations.
- **Dependencies**: None.

#### 4. Test Plan
- **Verification**:
  - Create a valid test fixture: `test-fixtures/valid-evaluator.json`.
  - Create an invalid test fixture: `test-fixtures/invalid-evaluator-missing-type.json`.
  - Run `bash promptops/validators/validate-evaluator.sh test-fixtures/valid-evaluator.json` (should pass).
  - Run `bash promptops/validators/validate-evaluator.sh test-fixtures/invalid-evaluator-missing-type.json` (should fail).
- **Success Criteria**: The validator script correctly passes valid configurations and rejects invalid ones based on the schema constraints.
- **Edge Cases**: Evaluator missing `id`, `type`, or `metrics` should be rejected. `type` must strictly be one of the allowed enum values.