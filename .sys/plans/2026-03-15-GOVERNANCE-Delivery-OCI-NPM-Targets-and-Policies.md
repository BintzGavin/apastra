#### 1. Context & Goal
- **Objective**: Implement missing OCI artifact and npm wrapper delivery target specifications, and missing takedowns and appeals policies.
- **Trigger**: `docs/vision.md` and `README.md` require declarative config describing how to sync approved versions to downstream systems, including target types OCI artifacts and npm/PyPI wrappers. It also mandates governance policies for takedown appeals.
- **Impact**: Enables governed distribution of prompt packages to OCI registries and npm, fulfilling the vision for delivery targets. Establishes clear procedures for content moderation appeals and takedowns.

#### 2. File Inventory
- **Create**:
  - `promptops/delivery/oci-target.yaml`: Declarative config describing how to sync approved versions to an OCI registry namespace.
  - `promptops/delivery/npm-target.yaml`: Declarative config describing how to sync approved versions to an npm package registry.
  - `promptops/policies/takedowns.md`: Policy detailing the takedown process.
  - `promptops/policies/appeals.md`: Policy detailing the appeals process.
- **Modify**:
  - `docs/status/GOVERNANCE.md`: Update version and append task completion log.
  - `docs/progress/GOVERNANCE.md`: Update version and append task completion log.
- **Read-Only**: `docs/vision.md` (delivery target section)

#### 3. Implementation Spec
- **Policy Architecture**: Delivery target specifications map an approved prompt promotion to registry publishing via configuration adapters. Policies provide manual guidelines.
- **Workflow Design**: No workflow changes; the existing `deliver.yml` will process these target files.
- **CODEOWNERS Patterns**: N/A
- **Promotion Record Format**: N/A
- **Delivery Target Format**: Both `promptops/delivery/oci-target.yaml` and `promptops/delivery/npm-target.yaml` should follow standard schema structures detailing type, registry, and channel fields.
  - `oci-target.yaml` type: `oci_artifact`
  - `npm-target.yaml` type: `npm_wrapper`
- **Dependencies**: CONTRACTS delivery schema must support `oci_artifact` and `npm_wrapper` types.

#### 4. Test Plan
- **Verification**: cat .github/CODEOWNERS
- **Success Criteria**: The spec dictates how the Executor will generate the missing target specs and policies.
- **Edge Cases**: Registry authentication configuration mismatch or missing schema validation.
