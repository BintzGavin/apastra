#### 1. Context & Goal
- **Objective**: Define the JSON schema and validation script for an "Approval state".
- **Trigger**: The `README.md` requires an "Approval state" (a machine-readable record that a revision/package passed required checks and human review), but the schema does not exist in `promptops/schemas/`.
- **Impact**: Unlocks GOVERNANCE workflows to automate promotion based on explicit, structured human and machine approvals.

#### 2. File Inventory
- **Create**:
  - `promptops/schemas/approval-state.schema.json` - JSON Schema defining the approval state format.
  - `promptops/validators/validate-approval-state.sh` - Bash script to execute the validation.
- **Modify**: []
- **Read-Only**:
  - `README.md`
  - `.jules/CONTRACTS.md`

#### 3. Implementation Spec
- **Schema Architecture**: A JSON Schema (`$id`: `apastra-approval-state-v1`) requiring `revision_ref` (string, target digest or ID), `checks_passed` (boolean), `human_review` (object with `reviewer` and `timestamp`), and `decision` (string, e.g., 'approved', 'rejected', 'abstained').
- **Content Digest Convention**: The digest is computed over canonical JSON via SHA-256 and stored in the `digest` field.
- **Pseudo-Code**: `validate-approval-state.sh` accepts a JSON file argument and executes `npx ajv-cli validate -s promptops/schemas/approval-state.schema.json -d "$1" --spec=draft2020 --strict=false`.
- **Public Contract Changes**: Exports the new schema `approval-state.schema.json`.
- **Dependencies**: None.

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
  npx ajv-cli validate -s promptops/schemas/approval-state.schema.json -d test-fixtures/valid-approval-state.json --spec=draft2020 --strict=false
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
  ! npx ajv-cli validate -s promptops/schemas/approval-state.schema.json -d test-fixtures/invalid-approval-state.json --spec=draft2020 --strict=false
  ```
