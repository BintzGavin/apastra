#### 1. Context & Goal
- **Objective**: Define JSON schemas and bash validators for the run request and run artifact outputs.
- **Trigger**: The README.md mandates a minimal BYO harness contract: "run request in → run artifact out". EVALUATION is currently blocked on `run-request.schema.json` and `run-artifact.schema.json` schemas.
- **Impact**: Unlocks the EVALUATION domain to start implementing the harness adapter runner and generating durable run artifacts.

#### 2. File Inventory
- **Create**:
  - `promptops/schemas/run-request.schema.json`
  - `promptops/schemas/run-artifact.schema.json`
  - Validation bash scripts in `promptops/validators/` for the run request and run artifact.
  - Test fixture JSON files in `test-fixtures/` for the run request and run artifact.
- **Modify**:
  - `docs/status/CONTRACTS.md`
- **Read-Only**:
  - `README.md`
  - `docs/status/EVALUATION.md`

#### 3. Implementation Spec
- **Schema Architecture**:
  - `run-request.schema.json` (JSON Schema): Required fields include `suite_id`, `revision_ref` (SHA/tag/digest), `model_matrix`, `evaluator_refs`. Optional fields: `trials`, `budgets`, `timeouts`, `artifact_backend_config`.
  - `run-artifact.schema.json` (JSON Schema): Required fields include a manifest, scorecard, cases, and failures. Manifest needs `input_refs`, `resolved_digests`, `timestamps`, `harness_version`, `model_ids`, `environment`, `status`. Scorecard needs `normalized_metrics`, `metric_definitions`. Cases should validate an array of case records with `case_id`, `per_trial_outputs`, `evaluator_outputs`.
- **Content Digest Convention**:
  - Run artifacts and requests are not themselves hashed into a digest field, but they will be content-addressed by the system.
- **Pseudo-Code**:
  - The validation scripts will use `npx ajv-cli validate` with `--spec=draft2020` and `--strict=false` for JSON files.
- **Public Contract Changes**:
  - Exports new schema IDs: `apastra-run-request-v1` and `apastra-run-artifact-v1`.
- **Dependencies**:
  - None. (EVALUATION depends on this task).

#### 4. Test Plan
- **Verification**:
  - Validation scripts in `promptops/validators/` should be run against test fixtures in `test-fixtures/`
- **Success Criteria**:
  - All validation scripts output `valid` and exit with code 0.
- **Edge Cases**:
  - Missing `suite_id` in run request should fail validation.
  - Missing `case_id` in cases array should fail validation.