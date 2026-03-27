#### 1. Context & Goal
- **Objective**: Implement cost budget governance policies to enforce cost limits on suites and flag runs that exceed thresholds before promotion.
- **Trigger**: `docs/vision.md` explicitly calls for "Cost budget governance" under "Expansion Governance Features" to enforce cost budget limits on suites and flag runs that exceed thresholds before promotion.
- **Impact**: Establishes a formal gate preventing the promotion of prompt packages that exceed organizational cost constraints, creating an auditable trail of cost policy enforcement.

#### 2. File Inventory
- **Create**:
  - `promptops/policies/cost-budget.md`: New append-only metadata store policy defining cost budget limits and escalation paths.
  - `promptops/schemas/cost-budget-record.schema.json`: New schema for the append-only cost budget records (Owned by CONTRACTS, but required for policy implementation).
- **Modify**: None.
- **Read-Only**: `docs/vision.md`, `README.md`, `promptops/schemas/suite.schema.json` (to understand suite cost_budget field).

#### 3. Implementation Spec
- **Policy Architecture**: The policy will mandate that any suite run exceeding the `cost_budget` defined in its suite spec MUST append a `cost-budget-record.schema.json` artifact. The workflow reads the `cost_delta` from the regression report or the `total_cost` from the run manifest and compares it to the budget. If exceeded, a `cost-budget-record` is appended, and downstream promotion is blocked unless a policy exception is granted.
- **Workflow Design**:
  - Trigger: `pull_request` on `promptops/prompts/**` or `promptops/datasets/**`.
  - Steps: Checkout, run suite, parse `scorecard.json` or `run_manifest.json` for cost, compare against `suite.yaml` `cost_budget`. If cost > budget, fail the check with an annotation.
- **CODEOWNERS Patterns**: No changes.
- **Promotion Record Format**: No changes.
- **Delivery Target Format**: No changes.
- **Dependencies**: CONTRACTS must provide `cost-budget-record.schema.json`.

#### 4. Test Plan
- **Verification**: Ensure the policy file is created in `promptops/policies/cost-budget.md` and aligns with the vision document.
- **Success Criteria**: The policy document clearly outlines the threshold enforcement, append-only record creation, and escalation path.
- **Edge Cases**: Missing cost data in the run artifact (gracefully skip or warn).
