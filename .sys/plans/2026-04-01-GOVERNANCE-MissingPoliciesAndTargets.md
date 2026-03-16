#### 1. Context & Goal
- **Objective**: Implement the missing delivery targets and missing policies required by the architecture vision.
- **Trigger**: `docs/vision.md` explicitly calls for "OCI artifacts, npm/PyPI wrappers" as delivery targets, and "takedowns.md, appeals.md" as governance policies for the public prompt library registry primitive.
- **Impact**: Enables OCI and ecosystem package registry delivery mechanisms, and establishes governance procedures for registry moderation, strengthening the system's governance and distribution capabilities.

#### 2. File Inventory
- **Create**: `promptops/policies/takedowns.md`, `promptops/policies/appeals.md`, `promptops/delivery/oci-target.yaml`, `promptops/delivery/npm-target.yaml`, `promptops/delivery/pypi-target.yaml`
- **Modify**: None
- **Read-Only**: `docs/vision.md`

#### 3. Implementation Spec
- **Policy Architecture**: The new policy files (`takedowns.md`, `appeals.md`) will define transparent processes for content removal requests and moderation decision appeals. The new delivery target specs (`oci-target.yaml`, `npm-target.yaml`, `pypi-target.yaml`) will provide configuration templates for publishing approved prompts to external registries.
- **Workflow Design**: None
- **CODEOWNERS Patterns**: None
- **Promotion Record Format**: None
- **Delivery Target Format**: YAML configurations conforming to the delivery target schema, specifying `type: oci`, `type: npm`, and `type: pypi` respectively, along with requisite registry details.
- **Dependencies**: CONTRACTS delivery target schema must support OCI, npm, and PyPI target types.

#### 4. Test Plan
- **Verification**: cat .sys/plans/2026-04-01-GOVERNANCE-MissingPoliciesAndTargets.md
- **Success Criteria**: The `.md` plan file is saved and ready for the executor.
- **Edge Cases**: None