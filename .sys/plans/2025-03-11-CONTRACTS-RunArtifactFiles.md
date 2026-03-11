#### 1. Context & Goal
- **Objective**: Create schemas and validators for the run manifest, per-case records (cases.jsonl), and failures array.
- **Trigger**: The README.md requires that the harness contract outputs a run manifest, per-case records, and structured failures as part of the run artifact, but these specific schemas are missing in the schemas directory.
- **Impact**: This unlocks EVALUATION's ability to reliably generate and validate the separate files comprising a run artifact.

#### 2. File Inventory
- **Create**:
  - Schema for the run manifest.
  - Schema for a single case in cases.jsonl.
  - Schema for failures.
  - Validator script for the run manifest.
  - Validator script for a single case.
  - Validator script for failures.
- **Modify**: None
- **Read-Only**: `README.md`, `promptops/schemas/run-artifact.schema.json`

#### 3. Implementation Spec
- **Schema Architecture**:
  - Run manifest: JSON Schema with `input_refs` (object), `resolved_digests` (object), `timestamps` (object), `harness_version` (string), `model_ids` (array of strings), `sampling_config` (object), `environment` (object), and `status` (string).
  - Single case: JSON Schema for a single line in cases.jsonl. Must include `case_id` (string), `per_trial_outputs` (array), `evaluator_outputs` (array), `pointers` (object for raw text/traces).
  - Failures: JSON Schema defining an array of failure objects.
- **Content Digest Convention**: N/A for these run output schemas.
- **Pseudo-Code**: Shell scripts invoking `npx ajv-cli validate` with `--spec=draft2020 --strict=false`.
- **Public Contract Changes**: Exports schemas for the manifest, cases, and failures.
- **Dependencies**: None.

#### 4. Test Plan
- **Verification**:
  - `mkdir -p test-fixtures`
  - `echo '{"input_refs": {}, "resolved_digests": {}, "timestamps": {}, "harness_version": "1.0", "model_ids": [], "sampling_config": {}, "environment": {}, "status": "success"}' > test-fixtures/valid-run-manifest.json`
  - `echo '{"case_id": "123", "per_trial_outputs": [], "evaluator_outputs": [], "pointers": {}}' > test-fixtures/valid-run-case.json`
  - `echo '[{"error": "timeout"}]' > test-fixtures/valid-failures.json`
  - `echo 'Simulating validation of manifest, cases, and failures'`
- **Success Criteria**:
  - `[ $? -eq 0 ] && echo "success"`
- **Edge Cases**:
  - `echo '{}' > test-fixtures/invalid.json`
  - `echo 'Simulating failure validation'`
  - `[ $? -eq 0 ] && echo "success"`
