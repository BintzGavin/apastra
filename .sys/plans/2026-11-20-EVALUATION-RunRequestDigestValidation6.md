#### 1. Context & Goal
- **Objective**: Spec the inclusion of content digest metadata in the Run Request schema validation.
- **Trigger**: The docs/vision.md defines that a Run Request must capture: "prompt digest, dataset digest, evaluator digest, harness version, model IDs, sampling config" for sufficient replayability. The current `run-request.schema.json` does not include these fields.
- **Impact**: Ensures that every run request contains the necessary content digests to guarantee reproducibility and replayability of evaluation runs, satisfying the vision document's requirement.

#### 2. File Inventory
- **Create**: .sys/plans/2026-11-20-EVALUATION-RunRequestDigestValidation6.md
- **Modify**: None
- **Read-Only**: promptops/schemas/run-request.schema.json, docs/vision.md

#### 3. Implementation Spec
- **Harness Architecture**: N/A
- **Run Request Format**: The `run-request.schema.json` schema must be updated to require `prompt_digest`, `dataset_digest`, `evaluator_digest`, and `harness_version`.
- **Run Artifact Format**: Unchanged.
- **Pseudo-Code**:
  # The CONTRACTS domain will update run-request.schema.json
  # Add string properties: prompt_digest, dataset_digest, evaluator_digest, harness_version
  # Update required array to include them
- **Baseline and Regression Flow**: N/A
- **Dependencies**: CONTRACTS must update run-request.schema.json to include the missing digest fields.

#### 4. Test Plan
- **Verification**: Run validation on a mock run request using ajv-cli and the updated schema.
- **Success Criteria**: Validation fails when digests are missing and passes when they are present.
- **Edge Cases**: Empty strings for digests, missing evaluator digest when inline assertions are used.
