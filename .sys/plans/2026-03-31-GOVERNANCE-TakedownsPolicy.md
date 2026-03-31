#### 1. Context & Goal
- **Objective**: Convert the generic takedowns stub into a formal append-only registry metadata store policy.
- **Trigger**: `docs/vision.md` specifically requires "Deprecation and takedown records" as append-only artifacts for the registry, but the existing `promptops/policies/takedowns.md` is a stub and lacks formal append-only mechanisms aligned with the `takedown-record.schema.json`.
- **Impact**: Ensures all takedown actions are formally governed, auditable, and tracked via an append-only JSON record format (`takedown-record.schema.json`), fulfilling the registry's trust and transparency requirements.

#### 2. File Inventory
- **Create**: .sys/plans/2026-03-31-GOVERNANCE-TakedownsPolicy.md
- **Modify**: promptops/policies/takedowns.md
- **Read-Only**: docs/vision.md, promptops/schemas/takedown-record.schema.json

#### 3. Implementation Spec
- **Policy Architecture**: Update `promptops/policies/takedowns.md` to define the formal takedown process. The policy will mandate that all takedowns must generate an append-only `takedown-record.schema.json` document stored in the metadata registry.
- **Workflow Design**: N/A
- **CODEOWNERS Patterns**: N/A
- **Promotion Record Format**: N/A
- **Delivery Target Format**: N/A
- **Dependencies**: Relies on `takedown-record.schema.json` from the CONTRACTS domain.

#### 4. Test Plan
- **Verification**: Review `.sys/plans/2026-03-31-GOVERNANCE-TakedownsPolicy.md`
- **Success Criteria**: The policy spec clearly defines the requirement to use the append-only `takedown-record.schema.json` format for all takedowns.
- **Edge Cases**: Malformed or missing schema fields, missing evidence, unverified reporter identities.
