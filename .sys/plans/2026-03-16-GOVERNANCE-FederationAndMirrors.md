#### 1. Context & Goal
- **Objective**: Specify the mirror protocol and optional federation policy.
- **Trigger**: `docs/vision.md` "Phase 5: Federation and mirrors" gap requires specifying a mirror protocol (sync by digest) and optional federation among multiple custodians.
- **Impact**: Establishes explicit governance rules for read-only mirrors and cross-custodian federation, enabling distributed discovery and verifiable prompt syncing without sacrificing trust or auditability.

#### 2. File Inventory
- **Create**:
  - `promptops/policies/federation.md`: Policy defining the requirements for syncing by digest and establishing federated trust across custodians.
  - `promptops/policies/mirroring.md`: Policy defining the requirements and process for running read-only mirrors.
- **Modify**:
  - `.github/CODEOWNERS`: Ensure `promptops/policies/federation.md` and `promptops/policies/mirroring.md` are reviewed by `@apastra/governance-admins`.
- **Read-Only**: `docs/vision.md` (specifically Phase 5 and Mirrors sections).

#### 3. Implementation Spec
- **Policy Architecture**:
  - `mirroring.md`: Define sync protocol relying on content-addressability (sync by digest). Define the requirements for an unofficial mirror vs an official mirror.
  - `federation.md`: Establish governance for cross-custodian trust, namespace resolution (e.g., `@custodian/prompt-id`), and shared protocol responsibilities.
- **Workflow Design**: None (this is a governance policy definition).
- **CODEOWNERS Patterns**: Ensure the new policies in `promptops/policies/` are owned by `@apastra/governance-admins`.
- **Promotion Record Format**: N/A
- **Delivery Target Format**: N/A
- **Dependencies**: None.

#### 4. Test Plan
- **Verification**: cat promptops/policies/federation.md promptops/policies/mirroring.md .github/CODEOWNERS
- **Success Criteria**: The `promptops/policies/federation.md` and `promptops/policies/mirroring.md` files exist and contain the necessary Phase 5 requirements from the vision document.
- **Edge Cases**: N/A.
