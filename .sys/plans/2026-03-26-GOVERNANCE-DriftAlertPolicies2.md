#### 1. Context & Goal
- **Objective**: Implement drift alert and escalation policies for canary suites.
- **Trigger**: `docs/vision.md` outlines "Drift alert policies" under Expansion Governance Features to manage canary suite failures.
- **Impact**: Establishes formal governance rules for how drift detection canary suite failures are escalated — including alert channels, escalation thresholds, and auto-rollback rules — ensuring post-ship quality erosion is formally managed.

#### 2. File Inventory
- **Create**: `promptops/policies/drift-alerts.md` (Formal policy document outlining drift alerts and escalation rules for canary suites)
- **Modify**: N/A
- **Read-Only**: `docs/vision.md` (Drift alert policies section)

#### 3. Implementation Spec
- **Policy Architecture**:
  - Define rules for when a canary suite run should trigger an alert (e.g., passing vs. failing thresholds).
  - Specify the required escalation paths (alert channels, responsibilities).
  - Outline conditions under which an auto-rollback (promotion of a prior digest) is mandated.
  - Require that all drift alerts are logged and auditable.
- **Workflow Design**: N/A (Policy document only)
- **CODEOWNERS Patterns**: Handled by existing `promptops/policies/` mapping to `@apastra/governance-admins`.
- **Promotion Record Format**: N/A
- **Delivery Target Format**: N/A
- **Dependencies**: CONTRACTS (drift report schemas, if applicable), EVALUATION (canary suite execution and drift reports).

#### 4. Test Plan
- **Verification**: Verify that `promptops/policies/drift-alerts.md` is created and accurately reflects the requirements outlined in `docs/vision.md` for drift alerts and escalation.
- **Success Criteria**: The drift alerts policy document is present in `promptops/policies/` and clearly defines thresholds, escalation paths, and auto-rollback rules.
- **Edge Cases**: Ensure the policy accounts for transient provider errors versus actual model drift.
