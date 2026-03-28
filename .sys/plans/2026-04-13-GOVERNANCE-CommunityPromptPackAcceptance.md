#### 1. Context & Goal
- **Objective**: Implement a governance policy document for community prompt pack acceptance.
- **Trigger**: `docs/vision.md` outlines "Community prompt pack acceptance policies: governance rules for accepting, reviewing, and publishing community-contributed prompt packs under a custodian org" under the Expansion Governance Features section.
- **Impact**: Establishes a formal governance pathway to bootstrap the public registry with community-contributed starter packs (e.g., summarization, extraction) while ensuring they meet automated security scans, schema validation, and human review criteria before being appended as immutable records.

#### 2. File Inventory
- **Create**:
  - `promptops/policies/community-prompt-pack-acceptance.md`: A governance policy document defining the submission, review, and acceptance criteria for community prompt packs.
- **Modify**:
  - None
- **Read-Only**:
  - `docs/vision.md` (for vision alignment)
  - `README.md`

#### 3. Implementation Spec
- **Policy Architecture**: Define the rules for accepting community prompt packs, which include passing automated security and schema scans, possessing a baseline dataset with passing evals, undergoing human custodian review, and ultimately being appended as immutable records if accepted.
- **Workflow Design**: Not applicable (this task creates a policy document, not an executable workflow).
- **CODEOWNERS Patterns**: The new policy file implicitly falls under the existing `promptops/policies/` mapping in `.github/CODEOWNERS` (assigned to `@apastra/governance-admins`).
- **Promotion Record Format**: Not applicable.
- **Delivery Target Format**: Not applicable.
- **Dependencies**: Requires CONTRACTS to supply validation schemas.

#### 4. Test Plan
- **Verification**: Run `ls -la promptops/policies/community-prompt-pack-acceptance.md` to ensure the file was created.
- **Success Criteria**: The `promptops/policies/community-prompt-pack-acceptance.md` file exists and accurately defines the acceptance criteria for community prompt packs as specified in the vision document.
- **Edge Cases**: N/A
