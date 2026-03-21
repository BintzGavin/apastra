#### 1. Context & Goal
- **Objective**: Implement run request validation logic against the CONTRACTS schema.
- **Trigger**: The EVALUATION domain was blocked waiting for `run-request.schema.json`, which is now available. This implements the "Run Request Format and validation" gap listed in `docs/vision.md` and `planning-evaluation.md`.
- **Impact**: Enables harness execution by ensuring inbound run requests are valid before processing.

#### 2. File Inventory
- **Create**: `.sys/plans/YYYY-MM-DD-EVALUATION-RunRequestValidation.md` (this file)
- **Modify**: None
- **Read-Only**: `promptops/schemas/run-request.schema.json`, `docs/vision.md`, `README.md`

#### 3. Implementation Spec
- **Harness Architecture**: N/A
- **Run Request Format**: Validates input against `promptops/schemas/run-request.schema.json`. Must contain suite ID, run ID, and configuration parameters.
- **Run Artifact Format**: N/A
- **Pseudo-Code**:
  - Read input `run_request.json`
  - Load schema `promptops/schemas/run-request.schema.json`
  - Use a JSON schema validator (e.g., `jsonschema` in Python or `ajv` in bash) to validate the input against the schema.
  - Return pass/fail status.
- **Baseline and Regression Flow**: N/A
- **Dependencies**: CONTRACTS schema (`promptops/schemas/run-request.schema.json`)

#### 4. Test Plan
- **Verification**: N/A
- **Success Criteria**: Validation script correctly identifies valid and invalid run requests.
- **Edge Cases**: Missing fields, invalid types.
