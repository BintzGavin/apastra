#### 1. Context & Goal
- **Objective**: Spec the inclusion of content digest metadata in the Run Request schema validation.
- **Trigger**: The docs/vision.md run request format requires prompt digest, dataset digest, and evaluator digest to be captured for reproducibility.
- **Impact**: Enables reproducible run artifacts and regression tracking by ensuring run requests contain the required digest metadata before execution.

#### 2. File Inventory
- **Create**: None
- **Modify**: None
- **Read-Only**: `docs/vision.md`, `promptops/schemas/run-request.schema.json`

#### 3. Implementation Spec
- **Harness Architecture**: The run request must include content digests for the prompt, dataset, and evaluators to ensure the exact inputs are recorded for the run.
- **Run Request Format**: Add `prompt_digest`, `dataset_digest`, and `evaluator_digests` to the run request schema.
- **Run Artifact Format**: N/A
- **Dependencies**: CONTRACTS (`promptops/schemas/run-request.schema.json`) must be updated to include these digest fields. RUNTIME resolver must provide the digests.

#### 4. Test Plan
- **Verification**: `jsonschema -i promptops/runs/run_request.json promptops/schemas/run-request.schema.json`
- **Success Criteria**: Validation fails if `prompt_digest`, `dataset_digest`, or `evaluator_digests` are missing, and passes when they are present.
- **Edge Cases**: Empty digests, invalid digest formats.
