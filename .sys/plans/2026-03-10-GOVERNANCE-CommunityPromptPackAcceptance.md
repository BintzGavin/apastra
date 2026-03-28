#### 1. Context & Goal
- **Objective**: Implement community prompt pack acceptance policy.
- **Trigger**: The docs/vision.md and planning instructions require "Community prompt pack acceptance policies: governance rules for accepting, reviewing, and publishing community-contributed prompt packs under a custodian org" as part of the public registry governance.
- **Impact**: Establishes a formal governance pathway to bootstrap the registry with community contributions while maintaining quality and security standards.

#### 2. File Inventory
- **Create**: `promptops/policies/community-prompt-pack-acceptance.md`
- **Modify**: None
- **Read-Only**: `docs/vision.md`, `README.md`

#### 3. Implementation Spec
- **Policy Architecture**: Creates a Markdown policy defining the lifecycle of a community prompt pack submission. The policy will dictate that community submissions must: 1) pass automated security and schema scans, 2) contain a baseline dataset with passing evals, 3) be reviewed by a human custodian, and 4) be appended as an immutable record if accepted.
- **Workflow Design**: Not applicable (this is a policy definition, not workflow implementation).
- **CODEOWNERS Patterns**: Handled by existing `.github/CODEOWNERS` (`promptops/policies/ @apastra/governance-admins`).
- **Promotion Record Format**: Not applicable.
- **Delivery Target Format**: Not applicable.
- **Dependencies**: Requires schemas from CONTRACTS for validation.

#### 4. Test Plan
- **Verification**: Run `wc -l promptops/policies/community-prompt-pack-acceptance.md` to ensure the file was created and is not empty. Review the content to ensure it covers submission, automated checks, human review, and acceptance criteria.
- **Success Criteria**: The policy file exists and correctly defines the acceptance criteria as described in the vision.
- **Edge Cases**: Submissions that fail automated checks but are functionally safe (requires explicit human override documented in policy).
