#### 1. Context & Goal
- **Objective**: Implement the Takedown Appeals Policy to govern appeals of moderation takedowns.
- **Trigger**: The `docs/vision.md` specifically requires "appeals" as a governance mechanism in the single-custodian registry model, but the existing `promptops/policies/appeals.md` is a stub and lacks formal append-only mechanisms aligned with the `takedown-appeal-record` schema.
- **Impact**: Enforces an auditable, append-only human checkpoint for overturning moderation decisions, establishing trust and transparency in the registry ecosystem.

#### 2. File Inventory
- **Create**: None
- **Modify**: `promptops/policies/appeals.md` (Update the stub with a formal append-only registry metadata store policy aligned with `takedown-appeal-record.schema.json`).
- **Read-Only**: `docs/vision.md`, `promptops/schemas/takedown-appeal-record.schema.json`

#### 3. Implementation Spec
- **Policy Architecture**: The policy must state that appeals are formally tracked as immutable `takedown-appeal-record.schema.json` artifacts in the registry metadata store. In-place modification of past moderation decisions is prohibited.
- **Workflow Design**: The policy defines the human checkpoint: an appellant files an appeal creating a `pending` record; a human governance maintainer reviews the evidence; the maintainer appends a new record with the status updated to `approved` or `rejected`.
- **CODEOWNERS Patterns**: Updates to the policy are governed by the `promptops/policies/ @apastra/governance-admins` boundary.
- **Promotion Record Format**: Not directly applicable to promotion records, but defines fields required in `takedown-appeal-record` (e.g., `appeal_id`, `takedown_record_id`, `status`).
- **Delivery Target Format**: Not applicable.
- **Dependencies**: CONTRACTS `takedown-appeal-record.schema.json`.

#### 4. Test Plan
- **Verification**: Verify the policy document exists and includes all required append-only principles and schema alignment.
- **Success Criteria**: `promptops/policies/appeals.md` contains a comprehensive governance policy for takedown appeals.
- **Edge Cases**: Appeals filed after 30 days are automatically rejected with a corresponding append-only record.
