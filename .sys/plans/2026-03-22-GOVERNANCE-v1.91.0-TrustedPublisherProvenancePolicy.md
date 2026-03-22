#### 1. Context & Goal
- **Objective**: Create a formal append-only policy for trusted publisher provenance.
- **Trigger**: `docs/vision.md` explicitly mentions "trusted publisher" badges with provenance requirements as a key governance pattern for the single-custodian registry, but the current `promptops/policies/trusted-publisher.md` is a generic placeholder and does not strictly align with the `trusted-publisher-provenance.schema.json` schema requirement for an append-only registry store.
- **Impact**: Establishes a verifiable, append-only trail for trusted publisher status, ensuring that every badge granted has a robust provenance record bridging the gap between governance and schema validation.

#### 2. File Inventory
- **Create**: None
- **Modify**:
  - `promptops/policies/trusted-publisher.md` (Update the generic document to formally specify append-only usage and align with `trusted-publisher-provenance.schema.json`)
- **Read-Only**:
  - `docs/vision.md` (To reference trusted publisher requirements)
  - `promptops/schemas/trusted-publisher-provenance.schema.json` (To ensure the policy strictly defines required fields and claims)

#### 3. Implementation Spec
- **Policy Architecture**:
  - The policy MUST state that trusted publisher status is governed via the append-only registry metadata store.
  - The policy MUST mandate the creation of a `trusted-publisher-provenance` JSON artifact containing `publisher_id`, `package_name`, `timestamp`, and `claims`.
  - The policy MUST specify that the `claims` object records verification statuses for `identity_verified`, `source_repo_linked`, and `build_environment_attested`.
  - Historical provenance claims MUST NEVER be modified or deleted in-place.
- **Workflow Design**: N/A
- **CODEOWNERS Patterns**: N/A
- **Promotion Record Format**: N/A
- **Delivery Target Format**: N/A
- **Dependencies**: Relies on `promptops/schemas/trusted-publisher-provenance.schema.json` from the CONTRACTS domain.

#### 4. Test Plan
- **Verification**: The executor will verify the markdown document is updated successfully at `promptops/policies/trusted-publisher.md` and contains the required append-only policy guidelines. Since this is a markdown policy, no automated test suite is required.
- **Success Criteria**: The `trusted-publisher.md` policy document exists and accurately describes the append-only tracking of trusted publisher provenance.
- **Edge Cases**: N/A for markdown policy creation.
