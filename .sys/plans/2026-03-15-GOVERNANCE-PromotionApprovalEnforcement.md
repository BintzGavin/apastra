#### 1. Context & Goal
- **Objective**: Enforce that a prompt package promotion requires a valid, matching Approval State record before proceeding.
- **Trigger**: The README.md requires human checkpoints where explicit approvals govern promotions, and that agents prepare promotion record PRs, but humans approve promotions.
- **Impact**: Ensures that promotions cannot be blindly executed without a cryptographic tie to a human decision, creating a strict audit trail linking the promotion binding back to the original human `approval-state`.

#### 2. File Inventory
- **Create**: None
- **Modify**:
  - `.github/workflows/promote.yml` (Will need to query `promptops-artifacts` branch for the approval records directory matching the input digest)
- **Read-Only**:
  - `promptops/schemas/approval-state.schema.json`
  - `promptops/schemas/promotion-record.schema.json`
  - `.github/workflows/record-approval.yml`

#### 3. Implementation Spec
- **Policy Architecture**: The promotion worker (GitHub Action) must read the `promptops-artifacts` branch, scan the approval records directory for a JSON record where `revision_ref` matches the input `$INPUT_DIGEST`. It must verify that `decision == "approved"` and `checks_passed == true`. If no valid record is found, the workflow must abort and fail the promotion.
- **Workflow Design**:
  1. In `promote.yml`, fetch and checkout the approval records directory from the `promptops-artifacts` branch.
  2. Add an `Enforce Approval` step before `Generate Promotion Record`.
  3. Extract the approval status using `jq`.
  4. If an approval is found, proceed. If no match is found, or if `decision != "approved"`, `exit 1` to fail the CI job.
- **CODEOWNERS Patterns**: No changes needed; existing `.github/CODEOWNERS` already enforces review boundaries.
- **Promotion Record Format**: No schema changes needed.
- **Delivery Target Format**: No schema changes needed.
- **Dependencies**: Relies on CONTRACTS `approval-state.schema.json` and the existing `promptops-artifacts` branch architecture.

#### 4. Test Plan
- **Verification**: Simulate the approval checking logic by mocking an approval file in the `test-fixtures` directory and testing the jq parsing.
  ```bash
  mkdir -p test-fixtures
  cat << 'MOCK' > test-fixtures/test-approval.json
  {
    "revision_ref": "sha256:abcd",
    "checks_passed": true,
    "decision": "approved",
    "human_review": {
      "reviewer": "alice",
      "timestamp": "2024-01-01T00:00:00Z"
    }
  }
  MOCK
  # Test approved case
  INPUT_DIGEST="sha256:abcd"
  APPROVED=$(jq -r --arg digest "$INPUT_DIGEST" 'select(.revision_ref == $digest and .decision == "approved" and .checks_passed == true) | .decision' test-fixtures/*.json | head -n 1)
  if [ "$APPROVED" != "approved" ]; then echo "Failed to detect approval"; exit 1; else echo "Approval detected successfully"; fi

  # Test unapproved case
  INPUT_DIGEST="sha256:none"
  APPROVED=$(jq -r --arg digest "$INPUT_DIGEST" 'select(.revision_ref == $digest and .decision == "approved" and .checks_passed == true) | .decision' test-fixtures/*.json | head -n 1)
  if [ "$APPROVED" == "approved" ]; then echo "Failed: detected phantom approval"; exit 1; else echo "Unapproved case handled correctly"; fi
  rm test-fixtures/test-approval.json
  ```
- **Success Criteria**: The bash snippet successfully identifies the mock approval for the correct digest and correctly rejects the missing digest.
- **Edge Cases**: Missing approval directory (must be created or gracefully ignored if checking), malformed JSON files, and multiple approval records for the same digest (should pick the most recent one or require all to be approved).
