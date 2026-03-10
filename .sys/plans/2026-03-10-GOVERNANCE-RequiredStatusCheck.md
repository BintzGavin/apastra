#### 1. Context & Goal
- **Objective**: Create a required status check workflow that gates pull request merges based on the pass/fail outcome of regression reports.
- **Trigger**: The README.md requires that "regression outcomes must gate merges" via "required status checks".
- **Impact**: Enforces quality thresholds by explicitly blocking PR merges that introduce regressions. It creates an audit trail linking the GitHub check status directly to the evaluation evidence in the regression report.

#### 2. File Inventory
- **Create**: `.github/workflows/regression-gate.yml` (GitHub Actions workflow to read regression reports and enforce the check status)
- **Create**: `promptops/policies/regression.yaml` (Base policy file defining absolute floors, allowed deltas, and directionality for metrics)
- **Read-Only**: `README.md` (Required status checks section), `derived-index/regressions/` (Directory containing regression reports produced by the EVALUATION domain)

#### 3. Implementation Spec
- **Policy Architecture**: The GitHub Actions workflow triggers on pull requests targeting protected branches. It locates the `regression_report.json` produced by the EVALUATION domain for the current commit in `derived-index/regressions/`. It parses the report's `status` field. If the status is a failure, the workflow exits with a non-zero code, thereby failing the required status check and blocking the merge.
- **Workflow Design**:
  - `on: [pull_request]`
  - `jobs.evaluate-regression`:
    - `steps:`
      - Checkout repository
      - Find the corresponding regression report in `derived-index/regressions/`
      - Read the `status` field from the report using `jq`
      - If `status == "fail"`, output a failure annotation and `exit 1`
      - If `status == "pass"`, output a success annotation and `exit 0`
- **CODEOWNERS Patterns**: Ensure `.github/CODEOWNERS` enforces review boundaries on `promptops/policies/` so regression thresholds cannot be softened without explicit human approval.
- **Promotion Record Format**: Not applicable.
- **Delivery Target Format**: Not applicable.
- **Dependencies**: The EVALUATION domain must provide a predictable and stable `regression_report.json` format. The CONTRACTS domain must define the schema for the regression policy.

#### 4. Test Plan
- **Verification**: Create a mock failing `regression_report.json` with `status: fail` and trigger the workflow. Verify that the workflow exits with 1.
- **Success Criteria**: The `regression-gate` job successfully fails and blocks the PR when a regression is detected, and passes when no regression is found.
- **Edge Cases**: If the regression report is missing, the workflow should fail closed (block the merge). If the baseline is ambiguous, it should warn and require signoff.