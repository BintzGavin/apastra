#### 1. Context & Goal
- **Objective**: Define the regression comparison engine that evaluates candidate runs against a baseline using GOVERNANCE policies.
- **Trigger**: `README.md` describes a regression report that compares a candidate scorecard to a baseline scorecard. The run-request pipeline is currently blocked on CONTRACTS schemas, so this is the next unblocked priority.
- **Impact**: Unlocks the ability to generate regression report files, which are required by the GOVERNANCE domain's required status check workflow to gate PRs.

#### 2. File Inventory
- **Create**:
  - `derived-index/regressions/` (Ensure directory exists for regression reports)
- **Modify**:
  - `docs/status/EVALUATION.md`
- **Read-Only**:
  - `promptops/policies/regression.yaml` (GOVERNANCE policy file)
  - `derived-index/baselines/`
  - `promptops/runs/` (for candidate run artifacts)

#### 3. Implementation Spec
- **Harness Architecture**: Not applicable; this is the comparison layer, not the harness execution layer.
- **Run Request Format**: Not applicable.
- **Run Artifact Format**: Not applicable.
- **Baseline and Regression Flow**:
  1. Retrieve the `regression.yaml` policy file from `promptops/policies/`.
  2. Retrieve the candidate scorecard from the target run artifact.
  3. Resolve the baseline run artifact digest from `derived-index/baselines/` and retrieve its scorecard.
  4. Compare candidate metrics against baseline metrics based on the policy rules (absolute floors, allowed deltas, directionality).
  5. Generate a regression report file containing pass/fail status, warnings, and evidence deltas.
  6. Store the report in `derived-index/regressions/`.
- **Dependencies**:
  - GOVERNANCE domain: `promptops/policies/regression.yaml` must exist.
  - EVALUATION domain: Assumes candidate run artifacts and baselines will exist.
  - CONTRACTS domain: Assumes schema for regression report output format will be provided.

#### 4. Test Plan
- **Verification**:
  ```bash
  echo 'No tests required'
  ```
- **Success Criteria**: The placeholder verification runs successfully.
- **Edge Cases**: Missing baseline, missing policy file, missing metrics in the scorecard.
