#### 1. Context & Goal
- **Objective**: Implement missing delivery target specifications (OCI, npm, PyPI) and missing moderation policies (takedowns, appeals).
- **Trigger**: `docs/vision.md` outlines delivery target types (OCI artifacts, npm/PyPI wrappers) and requires explicit moderation policies for takedowns and appeals.
- **Impact**: Fulfills the governance vision by providing mechanisms for handling malicious content via takedowns and appeals, and enables broader package distribution through diverse delivery targets.

#### 2. File Inventory
- **Create**:
  - `promptops/policies/takedowns.md` (Defines the process for removing violating packages)
  - `promptops/policies/appeals.md` (Defines the process for publishers to appeal a takedown decision)
  - `promptops/delivery/oci-target.yaml` (Declarative config for OCI registry sync)
  - `promptops/delivery/npm-target.yaml` (Declarative config for npm package wrapper sync)
  - `promptops/delivery/pypi-target.yaml` (Declarative config for PyPI package wrapper sync)
- **Modify**: None
- **Read-Only**: `docs/vision.md`, `README.md`

#### 3. Implementation Spec
- **Policy Architecture**: Moderation policies establish human checkpoints for emergency takedowns and appeals. Delivery targets define how approved versions sync to downstream systems.
- **Workflow Design**: N/A (Policies are human processes; targets are declarative configurations).
- **CODEOWNERS Patterns**: Existing `promptops/policies/` and `promptops/delivery/` patterns in `.github/CODEOWNERS` automatically cover these new files.
- **Promotion Record Format**: N/A
- **Delivery Target Format**:
  - `oci-target.yaml` specifies `type: oci` and registry details.
  - `npm-target.yaml` specifies `type: npm` and package scope details.
  - `pypi-target.yaml` specifies `type: pypi` and index details.
- **Dependencies**: Depends on CONTRACTS delivery target schema definition.

#### 4. Test Plan
- **Verification**: ls -l promptops/policies/takedowns.md promptops/policies/appeals.md promptops/delivery/oci-target.yaml promptops/delivery/npm-target.yaml promptops/delivery/pypi-target.yaml
- **Success Criteria**: All specified policy and delivery target files exist.
- **Edge Cases**: Missing parameters in delivery target specs.
