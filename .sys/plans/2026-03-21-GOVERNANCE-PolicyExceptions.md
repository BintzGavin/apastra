#### 1. Context & Goal
- **Objective**: Establish a policy defining how to handle exceptions to automated policy checks.
- **Trigger**: The vision doc explicitly lists "Policy exceptions" as a component of human checkpoints in the single-custodian registry model, but a formal policy defining them is missing.
- **Impact**: Enables a formal and auditable human escalation path to override blocking governance checks, providing flexibility for edge cases while ensuring strict oversight.

#### 2. File Inventory
- **Create**: `promptops/policies/policy-exceptions.md` (Defines the criteria and process for granting policy exceptions)
- **Modify**: None
- **Read-Only**: `docs/vision.md` (Human checkpoints section)

#### 3. Implementation Spec
- **Policy Architecture**: The `policy-exceptions.md` file will specify that any exception to an automated block requires explicit human review. Approved exceptions must be recorded as append-only records in the registry metadata store.
- **Workflow Design**: The policy will state that users must submit a GitHub issue requesting an exception. A designated approver from the `apastra/governance-admins` team must review and approve. Once approved, an append-only exception record will be recorded.
- **CODEOWNERS Patterns**: The policy itself and manual exception records must be reviewed by the governance admins.
- **Promotion Record Format**: N/A
- **Delivery Target Format**: N/A
- **Dependencies**: Depends on the existing moderation policy and automated check workflows that it will be overriding.
