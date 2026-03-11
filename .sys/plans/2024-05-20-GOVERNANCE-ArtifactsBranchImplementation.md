#### 1. Context & Goal
- **Objective**: Implement the Artifacts branch topology in governance workflows to store derived records off the main branch.
- **Trigger**: The README.md requires that derived, machine-generated artifacts (`runs/`, `reports/`, `promotions/`) are stored on an isolated branch named `promptops-artifacts` to reduce repo bloat and merge conflicts.
- **Impact**: Promotion records and regression reports will be isolated on `promptops-artifacts`.

#### 2. File Inventory
- **Create**: None
- **Modify**:
  - `.github/workflows/promote.yml`: Change checkout to fetch `promptops-artifacts`, append promotion to `promotions/`, and push back.
  - `.github/workflows/regression-gate.yml`: Add `fetch-depth: 2` to checkout. Fetch report from `promptops-artifacts` branch `reports/` directory instead of `derived-index/regressions/`.
- **Read-Only**: `README.md` (Artifacts branch topology section)

#### 3. Implementation Spec
- **Policy Architecture**: Workflows will explicitly manage cross-branch artifacts by pushing output and pulling requirements from `promptops-artifacts`.
- **Workflow Design**:
  - `promote.yml`: Checkout `promptops-artifacts`, create `promotions/`, append record, commit, and push.
  - `regression-gate.yml`: Checkout with `fetch-depth: 2`, retrieve `reports/regression_report.json` from the artifacts branch.
- **Dependencies**: EVALUATION's regression engine must output its reports to the `promptops-artifacts` branch.

#### 4. Test Plan
- **Verification**: `mkdir -p reports && echo '{"status":"pass"}' > reports/regression_report.json && jq -r .status reports/regression_report.json`
- **Success Criteria**: `[ "$(jq -r .status reports/regression_report.json)" = "pass" ] && echo "Regression passed."`
- **Edge Cases**: `rm -f reports/regression_report.json && [ ! -f reports/regression_report.json ] && echo "::warning::Regression report missing"`
