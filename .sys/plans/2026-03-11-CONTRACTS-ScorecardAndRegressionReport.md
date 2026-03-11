#### 1. Context & Goal
- **Objective**: Create the JSON schemas and validators for `scorecard.schema.json` and `regression-report.schema.json`.
- **Trigger**: The README.md requires scorecard and regression report schemas as the final core nouns for the CONTRACTS domain.
- **Impact**: This unlocks the EVALUATION and GOVERNANCE domains, which depend on normalized metrics and policy-evaluated comparison reports.

#### 2. File Inventory
- **Create**:
  - `promptops/schemas/scorecard.schema.json` (JSON schema for the scorecard output)
  - `promptops/schemas/regression-report.schema.json` (JSON schema for the regression report output)
  - `promptops/validators/validate-scorecard.sh` (bash script to validate the scorecard schema using `ajv-cli`)
  - `promptops/validators/validate-regression-report.sh` (bash script to validate the regression report schema using `ajv-cli`)
- **Modify**:
  - None
- **Read-Only**:
  - `README.md`
  - `promptops/schemas/run-artifact.schema.json`

#### 3. Implementation Spec
- **Schema Architecture**:
  - `scorecard.schema.json`: A JSON Schema (Draft 2020-12) defining a scorecard. Required fields include `normalized_metrics` (an object mapping metric names to their values) and `metric_definitions` (metadata like metric version and description). Optional fields may include variance details if trials were run.
  - `regression-report.schema.json`: A JSON Schema (Draft 2020-12) defining a regression report. Required fields include `status` (pass, fail, warning), `baseline_ref` (the reference digest or ID), `candidate_ref` (the digest or ID being tested), and `evidence` (a list of metric deltas and comparisons).
- **Content Digest Convention**: The output of these schemas (which are typically JSON) will be canonicalized via `jq -cSM .` and digested using `sha256sum`.
- **Pseudo-Code**:
  - `validate-scorecard.sh`: `npx ajv-cli validate -s promptops/schemas/scorecard.schema.json -d "$1" --spec=draft2020 --strict=false`
  - `validate-regression-report.sh`: `npx ajv-cli validate -s promptops/schemas/regression-report.schema.json -d "$1" --spec=draft2020 --strict=false`
- **Public Contract Changes**: Exports `apastra-scorecard-v1` and `apastra-regression-report-v1` schema IDs.
- **Dependencies**: The EVALUATION domain requires these schemas to format run artifact scorecards and compute regression reports.

#### 4. Test Plan
- **Verification**:
  - `echo '{"normalized_metrics": {"accuracy": 0.95}, "metric_definitions": {"accuracy": {"version": "v1", "description": "Percentage of correct answers"}}}' > test-fixtures/test-scorecard.json`
  - `./promptops/validators/validate-scorecard.sh test-fixtures/test-scorecard.json`
  - `echo '{"status": "pass", "baseline_ref": "sha256:abcd", "candidate_ref": "sha256:efgh", "evidence": []}' > test-fixtures/test-regression-report.json`
  - `./promptops/validators/validate-regression-report.sh test-fixtures/test-regression-report.json`
- **Success Criteria**:
  - `[ $? -eq 0 ]`
- **Edge Cases**:
  - `echo '{}' > test-fixtures/invalid-scorecard.json`
  - `./promptops/validators/validate-scorecard.sh test-fixtures/invalid-scorecard.json || true`
  - `[ $? -ne 0 ]`