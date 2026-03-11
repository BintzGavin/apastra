#### 1. Context & Goal
- **Objective**: Ensure the harness adapter output strictly complies with CONTRACTS schemas.
- **Trigger**: The Minimal BYO Harness Contract is defined in README.md, but the current runner shim script does not validate the specific output files (`run_manifest.json`, `scorecard.json`, `cases.jsonl`, `artifact_refs.json`, `failures.json`) against their schemas.
- **Impact**: Unlocks deterministic and schema-compliant evaluation artifacts for EVALUATION harnesses and GOVERNANCE policies.

#### 2. File Inventory
- **Create**: None
- **Modify**: `promptops/runtime/runner.py` (Update validation logic to check individual output files and their schemas).
- **Read-Only**: `README.md`, `promptops/schemas/run-manifest.schema.json`, `promptops/schemas/scorecard.schema.json`, `promptops/schemas/run-case.schema.json`, `promptops/schemas/artifact-refs.schema.json`, `promptops/schemas/run-failures.schema.json`

#### 3. Implementation Spec
- **Resolver Architecture**: Not applicable to this gap.
- **Manifest Format**: Not applicable.
- **Pseudo-Code**:
  - In `runner.py`, load the required schemas from `promptops/schemas/`.
  - After executing the entrypoint, verify the existence of `run_manifest.json`, `scorecard.json`, `cases.jsonl`, `artifact_refs.json`, and (if applicable) `failures.json` in the `output_dir`.
  - Validate each generated file against its corresponding schema using a JSON schema validator (like `jsonschema`).
  - Fail the execution with an informative error message if any file is missing or invalid.
- **Harness Contract Interface**: Input: `run_request.json` and adapter config, Output: structured run artifact directory (`run_manifest.json`, `scorecard.json`, `cases.jsonl`, `artifact_refs.json`, `failures.json`).
- **Dependencies**: `promptops/schemas/run-manifest.schema.json`, `promptops/schemas/scorecard.schema.json`, `promptops/schemas/run-case.schema.json`, `promptops/schemas/artifact-refs.schema.json`, `promptops/schemas/run-failures.schema.json`

#### 4. Test Plan
- **Verification**: Run a mock adapter that produces schema-compliant output files.
  ```bash
  mkdir -p test-fixtures
  echo '{"entrypoint": "echo Mock runner executed"}' > test-fixtures/mock_adapter.yaml
  echo '{"suite_id": "test_suite", "revision_ref": "v1", "model_matrix": ["gpt-4"], "evaluator_refs": []}' > test-fixtures/run_request.json
  mkdir -p test-fixtures/output
  python promptops/runtime/runner.py test-fixtures/run_request.json test-fixtures/mock_adapter.yaml test-fixtures/output
  ```
- **Success Criteria**: The runner script fails indicating that the required artifacts are missing, confirming the validation logic.
- **Edge Cases**: Missing files, invalid JSON structures, extra fields not allowed by schemas.
