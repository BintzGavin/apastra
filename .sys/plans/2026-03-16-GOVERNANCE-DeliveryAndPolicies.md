#### 1. Context & Goal
- **Objective**: Implement missing delivery target specifications for OCI and npm/PyPI, and establish moderation policies for takedowns and appeals.
- **Trigger**: `docs/vision.md` and `README.md` describe delivery targets (OCI artifacts, npm/PyPI wrappers) and transparent moderation procedures (takedowns, appeals) which are currently missing from the implementation.
- **Impact**: Enables governed distribution to standard package registries and provides explicit procedures for removing violating content and handling moderation disputes.

#### 2. File Inventory
- **Create**:
  - `promptops/delivery/oci-target.yaml`
  - `promptops/delivery/npm-target.yaml`
  - `promptops/delivery/pypi-target.yaml`
  - `promptops/policies/takedowns.md`
  - `promptops/policies/appeals.md`
- **Modify**: `.github/CODEOWNERS`
- **Read-Only**: `docs/vision.md`, `README.md`

#### 3. Implementation Spec
- **Policy Architecture**:
  - `promptops/policies/takedowns.md` will define criteria for immediate content removal (e.g., malware, severe PII violations) and response SLAs.
  - `promptops/policies/appeals.md` will document the process for publishers to dispute moderation actions.
- **Workflow Design**: No new workflows to design at this stage. This specifies the policy rules and target configs.
- **CODEOWNERS Patterns**:
  - Add `@apastra/governance-admins` to `.github/CODEOWNERS` for `promptops/policies/takedowns.md`.
  - Add `@apastra/governance-admins` to `.github/CODEOWNERS` for `promptops/policies/appeals.md`.
- **Promotion Record Format**: No changes.
- **Delivery Target Format**:
  - `promptops/delivery/oci-target.yaml` should define `type: oci`, `registry: registry.example.com`, and `channel: release`.
  - `promptops/delivery/npm-target.yaml` should define `type: npm`, `registry: npmjs.org`, and `channel: release`.
  - `promptops/delivery/pypi-target.yaml` should define `type: pypi`, `registry: pypi.org`, and `channel: release`.
- **Dependencies**: None.

#### 4. Test Plan
- **Verification**: ls -1 promptops/delivery/*-target.yaml promptops/policies/*.md
- **Success Criteria**: The output includes the newly created delivery target specs and policy files.
- **Edge Cases**: Missing delivery channels or unmapped reviewers.
