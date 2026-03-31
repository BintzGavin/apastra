#### 1. Context & Goal
- **Objective**: Implement a capability tagging governance policy to ensure evaluation suites broadly cover real-world failure modes.
- **Trigger**: The docs/vision.md explicitly requires capability tagging as a mitigation for False confidence where narrow suites miss real failures.
- **Impact**: Enforces that suites are tagged with specific capabilities, enabling governance gates to verify comprehensive coverage before promotion.

#### 2. File Inventory
- **Create**: promptops/policies/capability-tagging.md
- **Modify**: None
- **Read-Only**: docs/vision.md

#### 3. Implementation Spec
- **Policy Architecture**: Define the required taxonomy of capability tags (e.g., reasoning, extraction, safety) and establish a rule that Release-Candidate suites must demonstrate comprehensive capability coverage before promotion.
- **Workflow Design**: None
- **CODEOWNERS Patterns**: None
- **Promotion Record Format**: None
- **Delivery Target Format**: None
- **Dependencies**: The EVALUATION domain must add a tags or capabilities property to suite.schema.json.

#### 4. Test Plan
- **Verification**: Review promptops/policies/capability-tagging.md to ensure it explicitly defines the tagging taxonomy and coverage requirements.
- **Success Criteria**: The policy file is created and directly addresses the capability tagging mitigation.
- **Edge Cases**: Suites missing capability tags should be blocked from serving as release candidates.
