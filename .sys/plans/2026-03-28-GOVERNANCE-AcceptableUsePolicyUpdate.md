#### 1. Context & Goal
- **Objective**: Formalize the Acceptable Use Policy for the registry.
- **Trigger**: `docs/vision.md` explicitly mandates the publication of "Acceptable Use and deprecation policies for the registry, modeled after established platform patterns" in Phase 4 of the rollout plan. While `promptops/policies/acceptable-use.md` exists, it is a brief 4-line stub and lacks the formal structure, enforceability, and depth required for a platform-level moderation and governance policy as outlined in the vision.
- **Impact**: Establishes a robust, transparent, and enforceable Acceptable Use Policy that clearly defines prohibited content and conduct, serving as the foundational reference for community reporting, automated scans, and human moderation decisions.

#### 2. File Inventory
- **Create**: None
- **Modify**: `promptops/policies/acceptable-use.md`
- **Read-Only**: `docs/vision.md`

#### 3. Implementation Spec
- **Policy Architecture**:
  - Expand the policy to explicitly define prohibited content categories (e.g., CSAM, malware, hate speech, PII leaks, copyright infringement).
  - Outline the enforcement mechanisms (automated scans, community reports).
  - Specify the consequences of violation (e.g., takedown, registry ban, trusted publisher status revocation).
  - Ensure alignment with the single-custodian registry model's moderation procedures.
- **Workflow Design**: N/A
- **CODEOWNERS Patterns**: Handled by existing `promptops/policies/` mapping.
- **Promotion Record Format**: N/A
- **Delivery Target Format**: N/A
- **Dependencies**: N/A

#### 4. Test Plan
- **Verification**: Verify that `promptops/policies/acceptable-use.md` is expanded and accurately reflects comprehensive platform-level acceptable use standards.
- **Success Criteria**: The acceptable use policy document is comprehensive, unambiguous, and suitable for governing a public registry.
- **Edge Cases**: N/A
