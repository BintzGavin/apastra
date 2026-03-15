#### 1. Context & Goal
- **Objective**: Design the missing delivery target specifications for OCI and npm/PyPI wrappers and the missing moderation policies for takedowns and appeals.
- **Trigger**: `docs/vision.md` explicitly calls for "OCI artifacts, npm/PyPI wrappers" as delivery targets and "takedown appeals" policies for governed releases. These primitives do not currently exist in the implementation paths `promptops/delivery/` and `promptops/policies/`.
- **Impact**: Establishes full delivery capabilities for ecosystem-native distribution and finalizes the legal/governance framework for public moderation.

#### 2. File Inventory
- **Create**:
  - `promptops/delivery/oci-target.yaml`: Declarative config for OCI registry distribution.
  - `promptops/delivery/npm-target.yaml`: Declarative config for npm registry wrapper distribution.
  - `promptops/delivery/pypi-target.yaml`: Declarative config for PyPI wrapper distribution.
  - `promptops/policies/takedowns.md`: Policy defining takedown request and enforcement processes.
  - `promptops/policies/appeals.md`: Policy for appealing moderation/takedown decisions.
- **Modify**:
  - `docs/status/GOVERNANCE.md`: Update version and append task completion block.
  - `docs/progress/GOVERNANCE.md`: Update version and append task completion block.
- **Read-Only**: `docs/vision.md` (Section: Governed release packaging options, Moderation, governance), `promptops/delivery/prod-target.yaml`

#### 3. Implementation Spec
- **Policy Architecture**: The delivery targets declare external registries and credentials structure needed for the sync worker to push digested artifacts. The new policies expand the existing moderation suite to handle post-release legal and safety disputes.
- **Workflow Design**: No new workflows. The existing `deliver.yml` will interpret the new target types.
- **CODEOWNERS Patterns**: No new changes required, existing `@apastra/governance-admins` covers the new files in `promptops/delivery/` and `promptops/policies/`.
- **Promotion Record Format**: N/A
- **Delivery Target Format**:
  - OCI: Requires `type: oci_registry`, `registry_url`, `namespace`, `auth_strategy`.
  - npm: Requires `type: npm_registry`, `scope`, `auth_strategy`.
  - PyPI: Requires `type: pypi_registry`, `index_url`, `auth_strategy`.
- **Dependencies**: CONTRACTS must support the delivery target schema types `oci_registry`, `npm_registry`, `pypi_registry`.

#### 4. Test Plan
- **Verification**: `cat promptops/delivery/oci-target.yaml`
- **Success Criteria**: The delivery targets are correctly created with required fields matching the vision docs for distribution, and the takedown/appeals policies are created.
- **Edge Cases**: Registry URLs might be unreachable in CI, requiring dry-run support in the delivery worker.
