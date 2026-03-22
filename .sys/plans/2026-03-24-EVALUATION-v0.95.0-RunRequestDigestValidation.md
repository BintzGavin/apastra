#### 1. Context & Goal
The docs/vision.md defines that a Run Request must capture: "prompt digest, dataset digest, evaluator digest, harness version, model IDs, sampling config" for sufficient replayability. The current `run-request.schema.json` does not include these fields.
This ensures that every run request contains the necessary content digests to guarantee reproducibility and replayability of evaluation runs, satisfying the vision document's requirement.

#### 2. File Inventory
- promptops/schemas/run-request.schema.json
- docs/vision.md

#### 3. Implementation Spec
- **Harness Architecture**: N/A
- **Run Request Format**: The `run-request.schema.json` schema must be updated to require `prompt_digest`, `dataset_digest`, `evaluator_digest`, and `harness_version`.
- **Run Artifact Format**: Unchanged.
- **Dependencies**: CONTRACTS must update run-request.schema.json to include the missing digest fields.

#### 4. Test Plan
Create invalid test file:
```bash
cat << 'INNER_EOF' > test_invalid_run_request.json
{ "suite_id": "test", "revision_ref": "v1", "model_matrix": ["test-model"], "evaluator_refs": ["test-eval"] }
INNER_EOF
```
Create valid test file:
```bash
cat << 'INNER_EOF' > test_valid_run_request.json
{ "suite_id": "test", "revision_ref": "v1", "model_matrix": ["test-model"], "evaluator_refs": ["test-eval"], "prompt_digest": "sha256:123", "dataset_digest": "sha256:456", "evaluator_digest": "sha256:789", "harness_version": "1.0" }
INNER_EOF
```
Run `npx ajv-cli validate -s promptops/schemas/run-request.schema.json -d test_invalid_run_request.json` (should fail)
Run `npx ajv-cli validate -s promptops/schemas/run-request.schema.json -d test_valid_run_request.json` (should pass)
