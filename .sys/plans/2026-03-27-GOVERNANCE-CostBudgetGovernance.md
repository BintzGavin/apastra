#### 1. Context & Goal
- **Objective**: Implement cost budget governance policies to enforce cost limits on evaluation suites and flag runs that exceed thresholds before promotion.
- **Trigger**: `docs/vision.md` explicitly calls for "Cost budget governance" as a proposed expansion feature ("policies that enforce cost budget limits on suites and flag runs that exceed thresholds before promotion").
- **Impact**: Creates an auditable governance gate that prevents expensive or inefficient prompts from being promoted, ensuring cost control is enforced at the PR/merge level.

#### 2. File Inventory
- **Create**:
  - `promptops/policies/cost-budget-governance.md` - Policy document defining the rules for cost budget enforcement, thresholds, and escalation paths.
- **Modify**: None.
- **Read-Only**: `docs/vision.md` (for vision alignment), `README.md` (for context on suites and runs), CONTRACTS schemas (if applicable).

#### 3. Implementation Spec
- **Policy Architecture**: The policy will define how cost budgets are specified in suites, how runs are evaluated against these budgets, and the consequences of exceeding them (e.g., failing a required status check, requiring specific approval).
- **Workflow Design**: (Conceptual) A GitHub Actions workflow (like `regression-gate.yml`) would read the suite's `cost_budget` and compare it against the actual `cost` reported in the `run_manifest.json` or `scorecard.json`. If `cost > cost_budget`, the check fails.
- **CODEOWNERS Patterns**: The policy file itself will be owned by the GOVERNANCE domain.
- **Promotion Record Format**: No direct changes to the promotion record format are strictly necessary, though future iterations might include a `cost_approved` flag.
- **Delivery Target Format**: N/A
- **Dependencies**: Relies on EVALUATION/RUNTIME to accurately calculate and report `cost` in run artifacts, and CONTRACTS to support a `cost_budget` field in suite schemas.

#### 4. Test Plan
- **Verification**: Ensure the policy document is created and accurately reflects the requirements outlined in the vision.
- **Success Criteria**: The `promptops/policies/cost-budget-governance.md` file exists and contains a clear, actionable governance policy for cost budgets.
- **Edge Cases**: Handling cases where cost cannot be accurately estimated or where temporary exceptions are needed.
