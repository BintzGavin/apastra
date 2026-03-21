#### 1. Context & Goal
- **Objective**: Implement a governance policy defining the handling and structure of moderation decision records.
- **Trigger**: The docs/vision.md governance primitive for "Moderation decision records" as an append-only artifact is missing.
- **Impact**: Establishes a clear, auditable trail for all moderation actions, ensuring that decisions are traceable and immutable.

#### 2. File Inventory
- **Create**:
  - `promptops/policies/moderation-decision-records.md`: Defines the policy for moderation decision records.
- **Modify**: None
- **Read-Only**:
  - `docs/vision.md`: Sections on "Append-only artifacts" and "Moderation, governance, and legal/ToU considerations".
  - `promptops/policies/moderation-policy.md`: To understand the current moderation process.

#### 3. Implementation Spec
- **Policy Architecture**: The markdown document will specify that the registry must maintain moderation decision records as append-only, immutable artifacts. It will mandate that every moderation action (approval, rejection, takedown) generates a record detailing the action, the rationale, and the human checkpoint.
- **Workflow Design**: Not applicable. This implementation is purely a policy documentation gap.
- **CODEOWNERS Patterns**: Not applicable.
- **Promotion Record Format**: Not applicable.
- **Delivery Target Format**: Not applicable.
- **Dependencies**: Depends on existing moderation policies.
