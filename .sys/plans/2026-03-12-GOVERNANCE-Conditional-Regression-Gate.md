#### 1. Context & Goal
- **Objective**: Update `.github/workflows/regression-gate.yml` to conditionally skip the regression report check using `tj-actions/changed-files` for PRs that do not modify evaluable assets (prompts, harnesses, datasets, policies), preventing stalemates on docs-only PRs.
- **Trigger**: The regression gate currently enforces a strict failure if `reports/regression_report.json` is missing, which breaks PRs that legitimately have no evaluable changes and therefore produce no report.
- **Impact**: Enables docs-only and non-evaluable PRs to merge by gracefully skipping the check, while maintaining the strict `exit 1` block on missing reports for PRs that modify `promptops/harnesses/*`, `promptops/prompts/*`, `promptops/datasets/*`, or `promptops/policies/*`.

#### 2. File Inventory
- **Create**: None
- **Modify**: `.github/workflows/regression-gate.yml` - Add a step utilizing `tj-actions/changed-files` to determine if evaluable paths were modified, and conditionally execute or skip the regression status check steps based on this output.
- **Read-Only**: `.github/workflows/regression-gate.yml`

#### 3. Implementation Spec
- **Policy Architecture**: The workflow retains its role as a required status check on `main`. It will incorporate `tj-actions/changed-files` to assess whether files within `promptops/harnesses/**`, `promptops/prompts/**`, `promptops/datasets/**`, or `promptops/policies/**` were altered. If `steps.changed-files.outputs.any_changed == 'false'`, the workflow skips the report fetch and verification steps, effectively passing. If true, the workflow proceeds and maintains its strict failure condition if the report is absent.
- **Workflow Design**:
  1. Add an `id: changed-files` step utilizing `tj-actions/changed-files` configured with `files` pointing to `promptops/harnesses/**`, `promptops/prompts/**`, `promptops/datasets/**`, and `promptops/policies/**`.
  2. Append `if: steps.changed-files.outputs.any_changed == 'true'` to the existing `Fetch Artifacts Branch` and `Check Regression Report Status` steps.
  3. Introduce a new step that echoes "Skipping regression gate for non-evaluable changes." with the condition `if: steps.changed-files.outputs.any_changed == 'false'`.
- **CODEOWNERS Patterns**: N/A
- **Promotion Record Format**: N/A
- **Delivery Target Format**: N/A
- **Dependencies**: None.

#### 4. Test Plan
- **Verification**: Run `echo 'No tests required'` to fulfill test steps, as the planner does not run GitHub Actions.
- **Success Criteria**: The spec file is successfully created in `.sys/plans/`.
- **Edge Cases**: N/A