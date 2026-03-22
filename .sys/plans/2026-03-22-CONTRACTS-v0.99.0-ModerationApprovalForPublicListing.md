#### 1. Context & Goal
- **Objective**: Create the Moderation Approval for Public Listing schema and validation script.
- **Trigger**: `docs/vision.md` explicitly defines "Moderation approval for public listing" as a human checkpoint. A distinct schema is needed to formally capture this specific action.
- **Impact**: Enables the GOVERNANCE domain to implement procedures for moderation approval for public listings using a formal schema, preventing state hallucination.

#### 2. File Inventory
- **Create**:
  - `promptops/schemas/moderation-approval-for-public-listing.schema.json`: JSON Schema for moderation approval for public listing.
  - `promptops/validators/validate-moderation-approval-for-public-listing.sh`: Validation script for the schema.
- **Modify**:
  - `docs/status/CONTRACTS.md`: Update the existing entry for the current version from 'Planned' to 'Completed'.
  - `docs/progress/CONTRACTS.md`: Update the existing entry for the current version from 'Planned' to 'Completed'.
  - `.sys/llmdocs/context-contracts.md`: Register the new schema and validator.
  - `.jules/CONTRACTS.md`: Append a learning entry.
- **Read-Only**:
  - `docs/vision.md`
  - `promptops/schemas/moderation-decision-record.schema.json`

#### 3. Implementation Spec
- **Schema Architecture**:
  - Format: JSON Schema (Draft 2020-12).
  - Required fields: `approval_id`, `package_digest` (SHA-256 pattern), `approver_id`, `timestamp` (date-time format), and `listing_tier`.
- **Content Digest Convention**: N/A for this record.
- **Pseudo-Code**:
  - `validate-moderation-approval-for-public-listing.sh` uses `ajv validate -c ajv-formats --spec=draft2020 -s promptops/schemas/moderation-approval-for-public-listing.schema.json -d <target>` on temporary JSON converted files if needed, exiting non-zero on failure.
- **Public Contract Changes**: Exports `https://promptops.apastra.com/schemas/moderation-approval-for-public-listing.schema.json`
- **Dependencies**: None.

#### 4. Test Plan
- **Verification**: Run `TMP_TEST=$(mktemp); echo '{"approval_id": "test", "package_digest": "sha256:e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855", "approver_id": "user1", "timestamp": "2026-03-22T00:00:00Z", "listing_tier": "public"}' > $TMP_TEST; ajv validate -c ajv-formats --spec=draft2020 -s promptops/schemas/moderation-approval-for-public-listing.schema.json -d $TMP_TEST; rm -f $TMP_TEST`
- **Success Criteria**: The validator passes on valid records and fails on invalid records.
- **Edge Cases**: Missing approver_id, invalid digest format.
