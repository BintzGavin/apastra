#### 1. Context & Goal
- **Objective**: Implement a formal governance policy for quarantining flaky evaluation cases.
- **Trigger**: The vision document explicitly states "Quarantine flaky cases and track their flake rate; do not let flakiness silently pass as random noise" under "Benchmarking and evaluation best practices".
- **Impact**: Establishes a governed mechanism to prevent flaky evaluations from causing false-positive regression alerts, ensuring gating decisions remain trusted and deterministic.

#### 2. File Inventory
- **Create**: `promptops/policies/flake-quarantine.md` (Governs the quarantine of flaky test cases)
- **Modify**: `docs/status/GOVERNANCE.md` (Update version and log completion)
- **Read-Only**: `docs/vision.md` (Reference for "Quarantine flaky cases")

#### 3. Implementation Spec
- **Policy Architecture**:
  - The policy will define what constitutes a "flaky" case (e.g., inconsistent pass/fail across multiple trials without prompt changes).
  - It will mandate that flaky cases must be temporarily isolated into a "quarantine" dataset or marked as quarantined in their metadata.
  - Quarantined cases MUST NOT block promotions or trigger regression gates while under investigation.
  - Teams must track the flake rate and resolve the flakiness (e.g., improve evaluator logic, refine prompt, or fix non-determinism) before the case can be reinstated into the blocking regression suite.
  - This preserves the signal-to-noise ratio of the required status checks.
- **Workflow Design**: N/A (Policy document)
- **Dependencies**: Relies on EVALUATION's support for trials and tracking variance.

#### 4. Test Plan
- **Verification**: Ensure the `flake-quarantine.md` file exists and accurately reflects the governance rules for isolating flaky cases.
- **Success Criteria**: The policy document is successfully created in `promptops/policies/` and aligns with the vision document's requirements.
- **Edge Cases**: Ensure the policy specifies that quarantining a case is not a permanent bypass but a temporary measure requiring remediation.
