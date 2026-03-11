#### 1. Context & Goal
- **Objective**: Establish the workflow and format for creating and managing baselines.
- **Trigger**: The `README.md` defines a baseline as a "Named reference run/digest for regression comparison" and specifies it is "Stored in `derived-index/baselines/`". The run-request and regression engines depend on baselines.
- **Impact**: Without baselines, regression comparisons are impossible. This blocks the regression comparison engine and the GOVERNANCE policy evaluation that depends on it.

#### 2. File Inventory
- **Create**:
  - `derived-index/baselines/`
- **Modify**:
  - `docs/status/EVALUATION.md`
- **Read-Only**:
  - `promptops/schemas/run-artifact.schema.json`
  - `README.md`

#### 3. Implementation Spec
- **Harness Architecture**: Not applicable.
- **Run Request Format**: Not applicable.
- **Run Artifact Format**: Not applicable.
- **Baseline and Regression Flow**:
  - A baseline is a small file stored in `derived-index/baselines/<suite_id>/<name>.json`.
  - It acts as a named pointer to a specific, immutable run artifact.
  - Baselines are established explicitly, usually as a result of a "release candidate" run or a manual promotion. The first run of a suite implicitly becomes the initial candidate or requires a manual bootstrap run.
  - The format must capture the `suite_id`, `name`, `run_artifact_digest`, and `created_at`.
- **Dependencies**:
  - CONTRACTS domain schemas: `baseline.schema.json` must be defined.
  - GOVERNANCE domain: The baseline is the primary input (along with the candidate run) for the regression policy engine governed by GOVERNANCE.

#### 4. Test Plan
- **Verification**:
  ```bash
  echo 'No tests required'
  ```
- **Success Criteria**: The placeholder verification runs successfully.
- **Edge Cases**: Setting a baseline before a run artifact exists (requires bootstrap run).
