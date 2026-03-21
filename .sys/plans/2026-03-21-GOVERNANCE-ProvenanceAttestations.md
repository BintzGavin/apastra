#### 1. Context & Goal
- **Objective**: Implement a governance policy defining the handling, verification, and expectations of cryptographic signatures and build provenance attestations for prompt packages.
- **Trigger**: The docs/vision.md requires the registry to verify provenance attestations if provided, and otherwise mark them as "unsigned/unverified".
- **Impact**: Establishes clear, auditable rules for what constitutes valid provenance, ensuring supply-chain integrity for governed releases.

#### 2. File Inventory
- **Create**:
  - `promptops/policies/provenance-attestations.md`: Defines the policy for signatures and build provenance.
- **Modify**: None
- **Read-Only**:
  - `docs/vision.md`: Section on "Publishing, provenance, and signing".
  - `.github/workflows/immutable-release.yml`: To understand how attestations are currently generated.

#### 3. Implementation Spec
- **Policy Architecture**: The markdown document will specify that the registry relies on SLSA-style provenance or GitHub artifact attestations. It will mandate that valid signatures are verified against approved builder identities, and packages lacking them are flagged as "unsigned/unverified".
- **Workflow Design**: Not applicable. This implementation is purely a policy documentation gap.
- **CODEOWNERS Patterns**: Not applicable. The `promptops/policies/` directory is already covered.
- **Promotion Record Format**: Not applicable.
- **Delivery Target Format**: Not applicable.
- **Dependencies**: Depends on existing immutable-release workflows to generate attestations.
