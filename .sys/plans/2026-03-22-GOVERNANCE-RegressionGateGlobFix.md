#### 1. Context & Goal
- **Objective**: Fix regression-gate.yml file matching scope for promptops/policies to only include YAML files.
- **Trigger**: Broad glob patterns in the regression gate check currently include non-evaluable policy documents (markdown files), which erroneously triggers the check and blocks merges.
- **Impact**: Ensures the regression status check only gates PRs when functional policy schemas or evaluations change, preventing blocked merges for docs-only changes.

#### 2. File Inventory
- **Create**: None
- **Modify**: `.github/workflows/regression-gate.yml` to change `promptops/policies/**` to `promptops/policies/*.yaml`
- **Read-Only**: `promptops/policies/regression.yaml`, `docs/vision.md`

#### 3. Implementation Spec
- **Policy Architecture**: The Github Actions workflow will use a more restricted path match via the `tj-actions/changed-files` action to only match actual evaluation policies instead of governance text documentation.
- **Workflow Design**: Update `files` under `tj-actions/changed-files` action in `.github/workflows/regression-gate.yml`.
- **CODEOWNERS Patterns**: No changes.
- **Promotion Record Format**: No changes.
- **Delivery Target Format**: No changes.
- **Dependencies**: None.
