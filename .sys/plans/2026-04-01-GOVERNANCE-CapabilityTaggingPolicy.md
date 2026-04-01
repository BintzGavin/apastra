#### 1. Context & Goal
- **Objective**: Implement a capability tagging governance policy to ensure evaluation suites broadly cover real-world failure modes.
- **Trigger**: The docs/vision.md explicitly requires "capability tagging" as a mitigation for "False confidence" where narrow suites miss real failures.
- **Impact**: Enforces that suites are tagged with specific capabilities, enabling governance gates to verify comprehensive coverage before promotion.

#### 2. File Inventory
- **Create**: promptops/policies/capability-tagging.md
- **Modify**: []
- **Read-Only**: [docs/vision.md, promptops/schemas/suite.schema.json]

#### 3. Implementation Spec
- **Policy Architecture**: Define the required taxonomy of capability tags (e.g., reasoning, extraction, safety) and establish a rule that Release-Candidate suites must demonstrate comprehensive capability coverage before promotion.
- **Workflow Design**: N/A
- **CODEOWNERS Patterns**: N/A
- **Promotion Record Format**: N/A
- **Delivery Target Format**: N/A
- **Dependencies**: Depends on EVALUATION/CONTRACTS domain to eventually add a `tags` or `capabilities` property to suite.schema.json.

#### 4. Test Plan
- **Verification**: Ensure promptops/policies/capability-tagging.md is created and explicitly defines the capability taxonomy and coverage requirements for promotion.
- **Success Criteria**: The policy file is created and directly addresses the capability tagging mitigation from the vision document.
- **Edge Cases**: Suites missing capability tags should be flagged or blocked from serving as release candidates.
