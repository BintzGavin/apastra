#### 1. Context & Goal
- **Objective**: Spec the inclusion of content digest metadata in the Run Request schema validation to ensure reproducibility.
- **Trigger**: The docs/vision.md requires run requests to capture prompt digest, dataset digest, and evaluator digest for replayability.
- **Impact**: Unlocks deterministic replay of evaluations and ensures regression comparisons are anchored to immutable input states.

#### 2. File Inventory
- **Create**: None
- **Modify**: None
- **Read-Only**: promptops/schemas/run-request.schema.json, docs/vision.md

#### 3. Implementation Spec
- **Harness Architecture**: The harness adapter interface remains unchanged (input: run request; output: run artifact), but adapters must now pass through the new digest metadata from the request to the provenance attestation in the artifact.
- **Run Request Format**: Must include new required fields: `prompt_digest`, `dataset_digest`, and `evaluator_digest` (all strings, adhering to the digest convention).
- **Run Artifact Format**: Unchanged, but provenance metadata will now be populated with actual digests from the run request.
- **Pseudo-Code**:
  - Read incoming run request JSON.
  - Validate against the updated CONTRACTS `run-request.schema.json` which now requires digest fields.
  - Fail validation if any required digest field is missing or malformed.
  - Pass the validated digests to the harness adapter.
- **Baseline and Regression Flow**: Baselines and regression comparisons will now rely on the digests in the run artifact (populated from the request) to ensure they are comparing exact versions of prompts and datasets.
- **Dependencies**: CONTRACTS must update `promptops/schemas/run-request.schema.json` to include the new digest fields. RUNTIME resolver is unaffected.

#### 4. Test Plan
- **Verification**: Run `promptops/runs/validate-run-request.sh` on a mock run request containing the new digest fields.
- **Success Criteria**: The validation script exits with 0 and outputs "Valid" when given a request with all required digests.
- **Edge Cases**: Test validation failure when a digest is missing, or when a digest is malformed (e.g., wrong length or character set).
