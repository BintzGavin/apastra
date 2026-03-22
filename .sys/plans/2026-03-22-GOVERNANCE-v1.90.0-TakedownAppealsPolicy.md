#### 1. Context & Goal
- **Objective**: Create a formal append-only policy for takedown appeals.
- **Trigger**: `docs/vision.md` explicitly mentions "takedown appeals" as a key governance pattern modeled after established platform patterns, but the current `promptops/policies/appeals.md` is a generic placeholder and does not strictly align with the `takedown-appeal-record.schema.json` schema requirement for an append-only registry store.
- **Impact**: Establishes a verifiable, append-only trail for moderation appeals, ensuring that every appeal has a robust record bridging the gap between governance and schema validation.

#### 2. File Inventory
- **Create**: None
- **Modify**:
  - `promptops/policies/appeals.md` (Update the stub document to formally specify append-only usage and align with `takedown-appeal-record.schema.json`)
- **Read-Only**:
  - `docs/vision.md` (To reference takedown appeals requirements)
  - `promptops/schemas/takedown-appeal-record.schema.json` (To ensure the policy strictly defines required fields and statuses)

#### 3. Implementation Spec
- **Policy Architecture**:
  - The policy MUST state that appeals against takedown decisions are governed via the append-only registry metadata store.
  - The policy MUST mandate the creation of a `takedown-appeal-record` JSON artifact containing `appeal_id`, `takedown_record_id`, `appellant_id`, `reasoning`, and `status`.
  - The policy MUST specify that the initial state of the record is `pending`.
  - The policy MUST define the process for independent assessment resulting in a subsequent `takedown-appeal-record` being appended to transition the state to `approved` or `rejected`.
  - The policy MUST state that `evidence_links` is the preferred mechanism for supplying new contextual evidence.
  - Historical appeal claims MUST NEVER be modified or deleted in-place.
- **Workflow Design**: N/A
- **CODEOWNERS Patterns**: N/A
- **Promotion Record Format**: N/A
- **Delivery Target Format**: N/A
- **Dependencies**: Relies on `promptops/schemas/takedown-appeal-record.schema.json` from the CONTRACTS domain.

#### 4. Test Plan
- **Verification**: The executor will verify the markdown document is updated successfully at `promptops/policies/appeals.md` and contains the required append-only policy guidelines. Since this is a markdown policy, no automated test suite is required.
- **Success Criteria**: The `appeals.md` policy document exists and accurately describes the append-only tracking of takedown appeals.
- **Edge Cases**: N/A for markdown policy creation.
