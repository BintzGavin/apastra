#### 1. Context & Goal
- **Objective**: Define an automated workflow to record an "Approval state" when a revision or package passes required checks and human review.
- **Trigger**: The `README.md` requires an "Approval state" (a machine-readable record that a revision/package passed required checks and human review) to capture that human review and machine checks passed for a package.
- **Impact**: Establishes a machine-readable record of approvals, enabling downstream deployment to require both human signoff and CI passage.

#### 2. File Inventory
- **Create**: [A new GitHub Actions workflow to append approval records]
- **Modify**: []
- **Read-Only**: `README.md`, `promptops/schemas/approval-state.schema.json`

#### 3. Implementation Spec
- **Policy Architecture**: This workflow uses GitHub Actions `workflow_dispatch` to collect manual approval input. It also verifies `checks_passed` via the Checks API or a similar method before appending the record.
- **Workflow Design**:
  - Event: `workflow_dispatch` with inputs for `revision_ref` and `decision`.
  - Job: `record-approval`
  - Steps:
    - Checkout repository on `promptops-artifacts` branch.
    - Generate JSON file conforming to `apastra-approval-state-v1`.
    - Set `human_review.reviewer` to `github.actor` and `timestamp` to workflow execution time.
    - Commit and push to the repository.
- **Dependencies**: CONTRACTS must supply `promptops/schemas/approval-state.schema.json` (already implemented).

#### 4. Test Plan
- **Verification**:
  ```bash
  mkdir -p test-fixtures
  cat << 'INNER_EOF' > test-fixtures/valid-approval-state.json
  {
    "revision_ref": "sha256:example123",
    "checks_passed": true,
    "human_review": {
      "reviewer": "Alice",
      "timestamp": "2024-10-25T12:00:00Z"
    },
    "decision": "approved"
  }
  INNER_EOF
  npx --yes ajv-cli validate -s promptops/schemas/approval-state.schema.json -d test-fixtures/valid-approval-state.json --spec=draft2020 --strict=false
  ```
- **Success Criteria**:
  ```bash
  [ $? -eq 0 ] && echo "Success"
  ```
- **Edge Cases**:
  ```bash
  cat << 'INNER_EOF' > test-fixtures/invalid-approval-state.json
  {
    "revision_ref": "sha256:example123"
  }
  INNER_EOF
  ! npx --yes ajv-cli validate -s promptops/schemas/approval-state.schema.json -d test-fixtures/invalid-approval-state.json --spec=draft2020 --strict=false
  ```
