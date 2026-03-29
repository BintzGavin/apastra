#### 1. Context & Goal
- **Objective**: Convert the generic `promptops/policies/policy-exceptions.md` stub into a formal append-only registry metadata store policy that aligns with `policy-exception-record.schema.json`.
- **Trigger**: `docs/vision.md` specifically requires "Policy exceptions" as a human checkpoint in the registry metadata store, but the existing `promptops/policies/policy-exceptions.md` lacks formal append-only mechanisms aligned with the schema.
- **Impact**: Enforces a strict, auditable, append-only process for granting and tracking policy exceptions, ensuring transparency and accountability for any governance bypasses.

#### 2. File Inventory
- **Create**: None
- **Modify**: `promptops/policies/policy-exceptions.md` (convert to formal append-only policy matching schema)
- **Read-Only**: `docs/vision.md` (registry metadata store sections), `promptops/schemas/policy-exception-record.schema.json`

#### 3. Implementation Spec
- **Policy Architecture**:
  - Define policy exceptions as append-only records tracking overrides of blocking governance checks.
  - Require `exception_id`, `policy_id`, `target_digest`, `approver_id`, `reason`, and `timestamp` as mandated by `policy-exception-record.schema.json`.
  - Prohibit retroactive deletion or modification of exception records.
  - Require explicit human approval (e.g., via `@apastra/governance-admins` CODEOWNERS or an issue template workflow) for any exception.
- **Workflow Design**: (Pseudo-code)
  - Developer opens an exception request issue providing reason and target digest.
  - Governance admin reviews and approves the request.
  - Approved request triggers a workflow to generate a `policy-exception-record` JSON object.
  - Record is appended to the registry metadata store (e.g., `derived-index/exceptions/`).
- **CODEOWNERS Patterns**: Unchanged (governance team owns `promptops/policies/`).
- **Promotion Record Format**: N/A
- **Delivery Target Format**: N/A
- **Dependencies**: CONTRACTS `policy-exception-record.schema.json` format must be stable.

#### 4. Test Plan
- **Verification**: Review the updated `promptops/policies/policy-exceptions.md` to confirm it explicitly requires all schema fields and enforces append-only semantics.
- **Success Criteria**: The policy document explicitly matches the `policy-exception-record.schema.json` requirements and details the append-only recording process.
- **Edge Cases**: Missing approver (exception denied), malformed request (rejected), revoked exception (requires a new revocation record, not modification of the original).
