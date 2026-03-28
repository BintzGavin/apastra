#### 1. Context & Goal
- **Objective**: Define an artifact storage and retention policy.
- **Trigger**: docs/vision.md explicitly mentions that GitHub Actions artifacts default to 90-day retention and should not be treated as the long-term archive. A formal policy is missing.
- **Impact**: Ensures long-term auditability and durability of derived artifacts.

#### 2. File Inventory
- **Create**: promptops/policies/artifact-storage-retention.md
- **Modify**: None
- **Read-Only**: docs/vision.md

#### 3. Implementation Spec
- **Policy Architecture**: The policy will define that while GitHub Actions is the compute layer, long-term artifacts (e.g., traces, full cases.jsonl) must be synced to an external object store or OCI registry for compliance and audit replay, as GitHub artifacts expire in 90 days.
- **Workflow Design**: N/A (Policy document only)
- **CODEOWNERS Patterns**: Managed under `@apastra/governance-admins`
- **Promotion Record Format**: N/A
- **Delivery Target Format**: N/A
- **Dependencies**: None

#### 4. Test Plan
- **Verification**: Read the created policy file to ensure it aligns with the vision document's constraints on artifact retention.
- **Success Criteria**: The policy clearly states the 90-day limitation and the requirement for an external long-term archive.
- **Edge Cases**: N/A
