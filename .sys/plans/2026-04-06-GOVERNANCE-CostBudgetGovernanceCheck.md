#### 1. Context & Goal
- **Objective**: Implement a required status check workflow to enforce cost budgets on evaluation suites.
- **Trigger**: The vision doc specifies a `cost_budget` field on suites should hard-stop runs that exceed a dollar threshold, and the `cost-budget-governance.md` policy defines the enforcement rules.
- **Impact**: Enforces cost limits, preventing the promotion of prompts or configurations that exceed defined budget thresholds unless explicitly approved. Creates an auditable trail for cost constraint violations.

#### 2. File Inventory
- **Create**: `.sys/plans/2026-04-06-GOVERNANCE-CostBudgetGovernanceCheck.md`
- **Modify**: `.github/workflows/regression-gate.yml` (update to include the cost check step alongside the existing regression check)
- **Read-Only**: `docs/vision.md`, `README.md`, `promptops/policies/cost-budget-governance.md`, `promptops/schemas/suite.schema.json` (from CONTRACTS), `promptops/schemas/run-manifest.schema.json` and `promptops/schemas/scorecard.schema.json` (from CONTRACTS)

#### 3. Implementation Spec
- **Policy Architecture**: The regression gate workflow extracts the `cost_budget` from the suite definition and the `cost` from `run_manifest.json` (or `scorecard.json`). It compares them, posts a GitHub Check Run, and fails the job if `cost > cost_budget`.
- **Workflow Design**:
  - Event: `pull_request` on `promptops/**`
  - Step: For each suite, extract `cost_budget` from the suite file.
  - Step: Extract actual `cost` from `run_manifest.json` or `scorecard.json`.
  - Step: If `cost > cost_budget`, exit 1 and annotate the PR.
- **CODEOWNERS Patterns**: Overrides for cost budget failures require review from `@apastra/governance-admins` or designated budget owners, covered by existing CODEOWNERS paths.
- **Promotion Record Format**: N/A
- **Delivery Target Format**: N/A
- **Dependencies**: CONTRACTS must support `cost_budget` in `promptops/schemas/suite.schema.json`; EVALUATION/RUNTIME must emit `cost` in `run_manifest.json` or `scorecard.json`.

#### 4. Test Plan
- **Verification**: Create a mock suite with a low `cost_budget` and a mock run artifact with a high `cost`, then verify the GitHub Action fails the check and blocks the merge.
- **Success Criteria**: The regression gate workflow successfully extracts both values and correctly fails when the budget is exceeded, surfacing the violation in PR annotations.
- **Edge Cases**: Missing `cost_budget` in suite (pass/skip), missing `cost` in artifact (fail or skip depending on strictness), non-numeric values.
