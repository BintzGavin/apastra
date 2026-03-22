#### 1. Context & Goal
- **Objective**: Upgrade the ownership dispute policy to enforce an append-only registry metadata model for resolving canonical name conflicts.
- **Trigger**: `docs/vision.md` specifically requires the public registry governance to "Publish a transparent policy for naming, ownership disputes, takedown appeals, and deprecation." The current `promptops/policies/ownership-disputes.md` is a 3-line stub that lacks formal append-only mechanisms.
- **Impact**: Establishes a transparent, auditable process for claiming and resolving disputes over canonical prompt package names, generating `ownership-dispute-record` artifacts that consumers can verify.

#### 2. File Inventory
- **Create**: None
- **Modify**: `promptops/policies/ownership-disputes.md` (Rewrite the policy to align with the registry metadata architecture and require append-only records).
- **Read-Only**: `docs/vision.md` (registry governance section), `promptops/schemas/ownership-dispute-record.schema.json` (schema definitions for the required artifact).

#### 3. Implementation Spec
- **Policy Architecture**: The policy must define that all ownership disputes regarding canonical package namespaces are tracked via an immutable `ownership-dispute-record.schema.json` artifact appended to the registry metadata store.
- **Workflow Design**: The policy should mandate that when a dispute is opened, a record is created with status `open`. As the investigation progresses, new records are appended reflecting status transitions (`under_review`, `resolved`).
- **CODEOWNERS Patterns**: No changes required. The Governance Team remains the owner of policy files.
- **Promotion Record Format**: Not applicable.
- **Delivery Target Format**: Not applicable.
- **Dependencies**: Relies on the `ownership-dispute-record.schema.json` defined by CONTRACTS.

#### 4. Test Plan
- **Verification**: Ensure the updated policy document explicitly references the append-only `ownership-dispute-record` and prohibits in-place deletion of historical dispute claims.
- **Success Criteria**: The `promptops/policies/ownership-disputes.md` file contains a detailed, registry-aligned governance procedure matching the criteria defined in `docs/vision.md`.
- **Edge Cases**: The policy must describe the procedure for handling abandoned packages or disputes where the original owner is unresponsive.
