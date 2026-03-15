#### 1. Context & Goal
- **Objective**: Implement delivery target specifications for OCI artifacts, npm/PyPI wrappers, and missing moderation policies (takedowns, appeals).
- **Trigger**: `docs/vision.md` calls for optional packaging formats (OCI artifacts, npm/PyPI) for governed releases and a transparent policy for takedowns and appeals.
- **Impact**: Provides declarative configurations for syncing approved prompts to diverse distribution channels and formalizes moderation procedures.

#### 2. File Inventory
- **Create**:
  - `promptops/delivery/oci-target.yaml` (OCI artifact delivery target)
  - `promptops/delivery/npm-target.yaml` (npm registry delivery target)
  - `promptops/delivery/pypi-target.yaml` (PyPI registry delivery target)
  - `promptops/policies/takedowns.md` (Takedown policy)
  - `promptops/policies/appeals.md` (Appeals policy)
- **Modify**: None
- **Read-Only**: `docs/vision.md`, `README.md`

#### 3. Implementation Spec
- **Policy Architecture**: Delivery targets define declarative configurations detailing how to package and distribute prompt packages. Moderation policies define the rules for content takedowns and the appeals process.
- **Workflow Design**: Existing delivery workers will read these new target specifications.
- **CODEOWNERS Patterns**: The new files in `promptops/delivery/` and `promptops/policies/` are already covered by the existing `@apastra/governance-admins` ownership.
- **Promotion Record Format**: N/A
- **Delivery Target Format**:
  - `oci-target.yaml`: Declarative config for OCI registry syncing.
  - `npm-target.yaml`: Declarative config for npm registry syncing.
  - `pypi-target.yaml`: Declarative config for PyPI registry syncing.
- **Dependencies**: None.

#### 4. Test Plan
- **Verification**: echo 'No tests to run for Architect Planner'
- **Success Criteria**: The `.sys/plans/2026-03-15-GOVERNANCE-Delivery-Target-Specs.md` file correctly documents the missing delivery targets and moderation policies.
- **Edge Cases**: N/A
