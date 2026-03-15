#### 1. Context & Goal
- **Objective**: Add provenance requirements for “trusted publisher” badges.
- **Trigger**: `docs/vision.md` Phase 4 requires the addition of provenance requirements for “trusted publisher” badges.
- **Impact**: Establishes a verifiable mechanism to grant "trusted publisher" status based on cryptographically signed build provenance, increasing ecosystem security and trust.

#### 2. File Inventory
- **Create**: `promptops/policies/trusted-publisher.md` (Defines the policy and requirements for obtaining a trusted publisher badge)
- **Modify**: None
- **Read-Only**: `docs/vision.md` (Phase 4 Moderation and governance hardening)

#### 3. Implementation Spec
- **Policy Architecture**:
  - The `promptops/policies/trusted-publisher.md` policy document will define what a "trusted publisher" is and the exact criteria required to obtain the badge.
  - The core requirement is that packages must be published with valid SLSA/GitHub artifact attestations linking back to an approved organization/repository.
  - Submissions must pass automated moderation scans and adhere to the Acceptable Use Policy.
- **Workflow Design**: No new workflows to design at this stage. This specifies the policy rules.
- **CODEOWNERS Patterns**:
  - Add `@apastra/governance-admins` to `.github/CODEOWNERS` for `promptops/policies/trusted-publisher.md`.
- **Promotion Record Format**: No changes.
- **Delivery Target Format**: No changes.
- **Dependencies**: None.

#### 4. Test Plan
- **Verification**: `ls promptops/policies/trusted-publisher.md`
- **Success Criteria**: The `ls` command exits with code 0, indicating the policy file was successfully created.
- **Edge Cases**: None.
