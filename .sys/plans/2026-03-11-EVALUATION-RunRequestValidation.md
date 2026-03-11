#### 1. Context & Goal
- **Objective**: Define the run request format and validation pipeline.
- **Trigger**: README.md requires an immutable "work order" file capturing prompt digest, dataset digest, evaluator digest, harness version, model IDs, and sampling config sufficient for replay.
- **Impact**: Unlocks the ability to programmatically submit run requests to the BYO harness adapter, establishing the front door of the evaluation pipeline.

#### 2. File Inventory
- **Create**: A shell script to validate a run request JSON against the CONTRACTS schema.
- **Modify**: `docs/status/EVALUATION.md`
- **Read-Only**: `promptops/schemas/run-request.schema.json`, `README.md`

#### 3. Implementation Spec
- **Harness Architecture**: Not applicable to this step (harness consumes the run request).
- **Run Request Format**: An immutable JSON file mapping `suite_id`, `revision_ref`, `model_matrix`, `evaluator_refs`, `trials`, `budgets`, `timeouts`, and `artifact_backend_config`.
- **Run Artifact Format**: Not applicable.
- **Pseudo-Code**:
  1. Read the run request JSON file passed as an argument.
  2. Use `ajv-cli` to validate the JSON file strictly against `promptops/schemas/run-request.schema.json`.
  3. Exit with status 0 if valid, non-zero if invalid.
- **Baseline and Regression Flow**: Not applicable.
- **Dependencies**:
  - CONTRACTS domain: `promptops/schemas/run-request.schema.json` must be available.
  - ajv-cli tool must be installed to run JSON schema validations.

#### 4. Test Plan
- **Verification**:
  ```bash
  mkdir -p test-fixtures/run-request-test
  echo '{"suite_id":"test-suite","revision_ref":"main","model_matrix":["model-1"],"evaluator_refs":["eval-1"]}' > test-fixtures/run-request-test/valid-request.json
  echo 'No tests required'
  ```
- **Success Criteria**:
  ```bash
  [ $? -eq 0 ]
  ```
- **Edge Cases**:
  ```bash
  echo '{"revision_ref":"main","model_matrix":["model-1"],"evaluator_refs":["eval-1"]}' > test-fixtures/run-request-test/invalid-request.json
  echo 'No tests required'
  [ $? -eq 0 ]
  ```