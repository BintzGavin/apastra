#### 1. Context & Goal
- **Objective**: Create a JSON Schema definition for a Benchmark Suite (`suite.schema.json`).
- **Trigger**: The `README.md` defines a Suite as a core noun ("benchmark suite declaring datasets, evaluators, model/provider matrix, trials, budgets, and thresholds"), but `promptops/schemas/` currently lacks `suite.schema.json`.
- **Impact**: Unlocks the ability for harnesses to read deterministic, validated execution plans. Both RUNTIME and EVALUATION will depend on this schema to know what runs to execute.

#### 2. File Inventory
- **Create**:
  - `promptops/schemas/suite.schema.json`: The JSON Schema for the Suite definition.
  - `promptops/validators/validate-suite.sh`: Validation script for checking suites against the schema.
- **Modify**: []
- **Read-Only**:
  - `promptops/schemas/evaluator.schema.json`: To understand how evaluators are referenced.
  - `promptops/schemas/dataset-manifest.schema.json`: To understand how datasets are referenced.

#### 3. Implementation Spec
- **Schema Architecture**:
  - Format: JSON Schema (`draft2020-12` preferred).
  - Required fields: `id` (string), `name` (string), `datasets` (array of refs), `evaluators` (array of refs), `model_matrix` (array of model identifiers).
  - Optional fields: `description` (string), `trials` (integer, default 1), `budgets` (object specifying cost/time limits), `thresholds` (object defining pass/fail criteria for metrics).
- **Content Digest Convention**: The digest should be computed as a SHA-256 hash of the canonicalized JSON representation of the suite. The schema should not enforce the digest field on the suite itself but it will be computed dynamically by harnesses.
- **Pseudo-Code**:
  ```
  // validate-suite.sh pseudo-code
  load suite.schema.json
  for file in promptops/suites/*.json; do
    ajv-cli validate -s promptops/schemas/suite.schema.json -d $file
  done
  ```
- **Public Contract Changes**: Exported schema ID will be `https://apastra.com/schemas/promptops/suite.schema.json`.
- **Dependencies**: None. (Prompt spec, Dataset, and Evaluator schemas are complete according to `docs/status/CONTRACTS.md` v0.4.0).

#### 4. Test Plan
- **Verification**: `npx ajv-cli validate -s promptops/schemas/suite.schema.json -d test-fixtures/valid-suite.json --spec=draft2020 --strict=false`
- **Success Criteria**: The `ajv-cli` command exits with `0` (success) when a valid `test-fixtures/valid-suite.json` is provided, and fails appropriately on invalid fixtures.
- **Edge Cases**: Missing required fields (`model_matrix`, `evaluators`, `datasets`), invalid types for `trials` (e.g., negative integers), or incorrect structure for `budgets`/`thresholds`.