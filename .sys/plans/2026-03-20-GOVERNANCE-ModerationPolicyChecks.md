#### 1. Context & Goal
- **Objective**: Establish a policy and workflow for moderation and policy checks centrally.
- **Trigger**: `docs/vision.md` explicitly calls for moderation and policy checks centrally, which requires documentation and formal processes.
- **Impact**: Provides an auditable trail for flagging moderation and policy check failures, preventing downstream delivery and warning consumers.

#### 2. File Inventory
- **Create**:
  - `promptops/policies/moderation-policy.md`: Policy defining what constitutes a moderation or policy failure, how it is reported, and how flags are applied.
- **Modify**: None
- **Read-Only**: `docs/vision.md`

#### 3. Implementation Spec
- **Policy Architecture**: The policy defines the criteria for moderation and policy check failures, the automated scanning requirements, and the human escalation path for manual flagging.
- **Workflow Design**: Defines how flags are appended to the registry metadata store as immutable records, ensuring consumers can query the flag status before usage.
- **CODEOWNERS Patterns**: `promptops/policies/moderation-policy.md` owned by `@apastra/governance-admins`
- **Promotion Record Format**: N/A
- **Delivery Target Format**: N/A
- **Dependencies**: None
