#### 1. Context & Goal
- **Objective**: Create a required status check workflow to gate merges on regression pass/fail outcomes.
- **Trigger**: The README.md requires "Branch protections require checks to pass before merging to protected branches" and "Regression outcomes must gate merges", but no such workflow exists in `.github/workflows/`.
- **Impact**: Enforces a strict gate on pull requests, ensuring that no prompt or model changes are merged if they degrade baseline performance. Creates an auditable trail connecting PR merges to explicit `regression_report.json` outcomes.

#### 2. File Inventory
- **Create**: A new GitHub Actions workflow file in `.github/workflows/` (to read the regression report and post a commit status check)
- **Modify**: None
- **Read-Only**: `derived-index/regressions/regression_report.json` (EVALUATION domain output to read), `promptops/schemas/regression-report.schema.json` (CONTRACTS domain schema to understand the report format)

#### 3. Implementation Spec
- **Policy Architecture**: The GitHub Actions workflow will trigger on `pull_request` against the default branch. It will read `derived-index/regressions/regression_report.json`, extract the `status` field, and use the GitHub Checks API (or `gh api` CLI) to post a passing or failing status check on the PR's HEAD commit based on whether the status is "pass" or "fail".
- **Workflow Design**:
  - `on: [pull_request]`
  - `jobs: gate:`
  - `steps:`
    - Checkout code
    - Read `derived-index/regressions/regression_report.json`
    - Check if `jq -r .status derived-index/regressions/regression_report.json` equals `pass`
    - If `pass`, emit a successful status to the GitHub API for the current commit.
    - If `fail` or `warning`, emit a failing status to the GitHub API, failing the workflow job and blocking the merge.
- **Dependencies**: Depends on the EVALUATION domain reliably producing `derived-index/regressions/regression_report.json` matching `promptops/schemas/regression-report.schema.json`.

#### 4. Test Plan
- **Verification**:
  - `mkdir -p derived-index/regressions/`
  - `echo '{"status": "fail", "baseline_ref": "v1", "candidate_ref": "v2", "evidence": []}' > derived-index/regressions/regression_report.json`
  - `jq -r .status derived-index/regressions/regression_report.json`
  - `[ $(jq -r .status derived-index/regressions/regression_report.json) != "pass" ]`
  - `echo '{"status": "pass", "baseline_ref": "v1", "candidate_ref": "v2", "evidence": []}' > derived-index/regressions/regression_report.json`
  - `jq -r .status derived-index/regressions/regression_report.json`
  - `[ $(jq -r .status derived-index/regressions/regression_report.json) = "pass" ]`
- **Success Criteria**:
  - `echo '{"status": "pass", "baseline_ref": "v1", "candidate_ref": "v2", "evidence": []}' > derived-index/regressions/regression_report.json`
  - `STATUS=$(jq -r .status derived-index/regressions/regression_report.json)`
  - `[ "$STATUS" = "pass" ]`
- **Edge Cases**:
  - `rm -f derived-index/regressions/regression_report.json`
  - `! test -f derived-index/regressions/regression_report.json`
