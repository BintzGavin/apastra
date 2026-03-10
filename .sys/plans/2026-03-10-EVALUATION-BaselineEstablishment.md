#### 1. Context & Goal
- **Objective**: Establish the workflow and format for creating and managing baselines.
- **Trigger**: The `README.md` defines a baseline as a "Named reference run/digest for regression comparison" and specifies it is "Stored in `derived-index/baselines/`". Currently, `derived-index/baselines/` is empty and no process exists for setting a baseline.
- **Impact**: Without baselines, regression comparisons are impossible. This blocks the regression comparison engine and the GOVERNANCE policy evaluation that depends on it. Establishing a baseline format unblocks the regression workflow.

#### 2. File Inventory
- **Create**:
  - `promptops/schemas/baseline.schema.json`: Schema defining the format of a baseline reference file.
  - `derived-index/baselines/`: Directory to store the baseline files (ensure it exists).
- **Modify**:
  - `docs/status/EVALUATION.md`: Update to reflect work on baselines.
- **Read-Only**:
  - `README.md`: Consulted for baseline definition ("Named reference run/digest for regression comparison", "Stored in `derived-index/baselines/`").
  - `promptops/schemas/run-artifact.schema.json`: Required to understand the artifact digest that the baseline will point to.

#### 3. Implementation Spec
- **Baseline Architecture**:
  - A baseline is a small file stored in `derived-index/baselines/`.
  - It acts as a named pointer to a specific, immutable run artifact.
  - Baselines are established explicitly, usually as a result of a "release candidate" run or a manual promotion.
- **Baseline Format** (`baseline.schema.json`):
  - `suite_id`: The ID of the benchmark suite this baseline applies to.
  - `name`: A human-readable name for the baseline (e.g., "prod-current", "v1.2-release").
  - `run_artifact_digest`: The content digest of the `run_manifest.json` (or the aggregate artifact digest) of the run that serves as the baseline.
  - `created_at`: Timestamp of baseline establishment.
  - `metadata`: Optional field for recording context (e.g., the PR that triggered the baseline, the person who approved it).
- **Pseudo-Code**:
  ```bash
  # Pseudo-code for establishing a baseline via CLI
  promptops establish-baseline --suite-id "my-suite" --name "prod-current" --run-digest "sha256:abcd..."

  # This generates a file like derived-index/baselines/my-suite/prod-current.json
  {
    "suite_id": "my-suite",
    "name": "prod-current",
    "run_artifact_digest": "sha256:abcd...",
    "created_at": "2026-03-10T12:00:00Z"
  }
  ```
- **Dependencies**:
  - **CONTRACTS**: Depends on the existence of `run-artifact.schema.json` so the baseline has a target to point to.
  - **GOVERNANCE**: The baseline is the primary input (along with the candidate run) for the regression policy engine governed by GOVERNANCE.

#### 4. Test Plan
- **Verification**: Run schema validation on a dummy baseline file using the newly created `baseline.schema.json` to ensure it enforces the required fields (suite_id, name, run_artifact_digest).
- **Success Criteria**: The dummy baseline file successfully validates against the schema, confirming the structure is correctly defined.
- **Edge Cases**:
  - Attempting to set a baseline with a missing or invalid digest format.
  - Overwriting an existing baseline name (baselines should generally be immutable or explicitly rotated).
  - The "cold start" problem: ensuring documentation states that the first run must be explicitly designated as the initial baseline.