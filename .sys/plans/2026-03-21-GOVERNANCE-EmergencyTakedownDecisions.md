#### 1. Context & Goal
- **Objective**: Implement the Emergency Takedown Decisions governance policy.
- **Trigger**: The `docs/vision.md` explicitly mentions "Emergency takedown decisions" as a core human checkpoint, but no corresponding policy exists in `promptops/policies/`.
- **Impact**: Enforces formal human checkpoints and ensures an auditable trail when critical moderation and legal actions necessitate an immediate bypass of standard review timelines to remove a package.

#### 2. File Inventory
- **Create**: `promptops/policies/emergency-takedown-decisions.md` (Formal policy defining the criteria, process, and required records for emergency takedowns).
- **Modify**: None.
- **Read-Only**: `docs/vision.md`, `promptops/schemas/takedown-record.schema.json`.

#### 3. Implementation Spec
- **Policy Architecture**: The policy will mandate that emergency takedowns bypass standard 48-hour review periods due to severe, immediate risk (e.g., explicit CSAM, active malware propagation, or immediate legal injunction). The action must be authorized by a senior governance maintainer and must immediately append a `takedown-record.schema.json` document to the registry metadata store.
- **Workflow Design**: Emergency takedown reports require an immediate out-of-band alert to governance administrators. Upon validation, the admin directly commits the takedown record to the repository.
- **CODEOWNERS Patterns**: The policy file will fall under the existing `promptops/policies/ @apastra/governance-admins` boundary.
- **Promotion Record Format**: N/A
- **Delivery Target Format**: N/A
- **Dependencies**: Relies on `takedown-record.schema.json` to format the resulting artifact.

#### 4. Test Plan
- **Verification**: Review the generated `promptops/policies/emergency-takedown-decisions.md` document.
- **Success Criteria**: The policy accurately reflects the "Emergency takedown decisions" checkpoint required by the vision document, explicitly binding the human decision to the creation of a takedown record.
- **Edge Cases**: Instances where the emergency criteria are not met must gracefully fall back to the standard `takedown.md` process.
