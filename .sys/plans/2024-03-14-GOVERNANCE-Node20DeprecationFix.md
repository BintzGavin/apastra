#### 1. Context & Goal
- **Objective**: Fix Node.js 20 deprecation warnings in GitHub Actions workflows.
- **Trigger**: GitHub Actions environment deprecation warnings for Node.js 20 affecting javascript actions like `actions/checkout@v4` and `tj-actions/changed-files@v44`.
- **Impact**: Ensures CI stability, removes workflow warnings, and aligns execution environment with maintained Node versions.

#### 2. File Inventory
- **Create**: None
- **Modify**:
  - `.github/workflows/auto-merge.yml`: Inject `FORCE_JAVASCRIPT_ACTIONS_TO_NODE24: true` into job `env`.
  - `.github/workflows/community-reporting.yml`: Inject `FORCE_JAVASCRIPT_ACTIONS_TO_NODE24: true` into job `env`.
  - `.github/workflows/deliver.yml`: Inject `FORCE_JAVASCRIPT_ACTIONS_TO_NODE24: true` into job `env`.
  - `.github/workflows/immutable-release.yml`: Inject `FORCE_JAVASCRIPT_ACTIONS_TO_NODE24: true` into job `env`.
  - `.github/workflows/moderation-scan.yml`: Inject `FORCE_JAVASCRIPT_ACTIONS_TO_NODE24: true` into job `env`.
  - `.github/workflows/promote.yml`: Inject `FORCE_JAVASCRIPT_ACTIONS_TO_NODE24: true` into job `env`.
  - `.github/workflows/record-approval.yml`: Inject `FORCE_JAVASCRIPT_ACTIONS_TO_NODE24: true` into job `env`.
  - `.github/workflows/regression-gate.yml`: Inject `FORCE_JAVASCRIPT_ACTIONS_TO_NODE24: true` into job `env`.
  - `.github/workflows/secret-scan.yml`: Inject `FORCE_JAVASCRIPT_ACTIONS_TO_NODE24: true` into job `env`.
- **Read-Only**: None

#### 3. Implementation Spec
- **Workflow Design**:
  For every workflow job listed above, inject the environment variable `FORCE_JAVASCRIPT_ACTIONS_TO_NODE24: true` at the job level.
  Example pseudo-code structure:
  ```yaml
  jobs:
    job-name:
      runs-on: ubuntu-latest
      env:
        FORCE_JAVASCRIPT_ACTIONS_TO_NODE24: true
  ```
- **Dependencies**: None

#### 4. Test Plan
- **Verification**: Run `grep -r "FORCE_JAVASCRIPT_ACTIONS_TO_NODE24" .github/workflows/` to confirm all modified workflows contain the injected `env` variable.
- **Success Criteria**: The `grep` command successfully finds the environment variable in all targeted workflow files.
- **Edge Cases**: Workflows with existing `env` blocks must properly merge the new variable rather than overwriting existing ones.
