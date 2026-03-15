#### 1. Context & Goal
- **Objective**: Design additional delivery target specs for OCI artifacts and registry wrappers to close the packaging gap described in the vision.
- **Trigger**: `docs/vision.md` explicitly calls for optional governed packaging including OCI artifacts and ecosystem wrappers (npm/PyPI). Currently, only `promptops/delivery/prod-target.yaml` (a GitHub PR target) exists.
- **Impact**: Enables governed distribution via digest-addressed OCI artifacts and language ecosystem registries (npm/PyPI), completing the delivery options promised in the vision.

#### 2. File Inventory
- **Create**:
  - `promptops/delivery/oci-target.yaml` (Spec for OCI artifact distribution)
  - `promptops/delivery/npm-target.yaml` (Spec for npm registry distribution)
- **Modify**:
  - `docs/status/GOVERNANCE.md` (Add completed task entry)
  - `docs/progress/GOVERNANCE.md` (Add completed task entry)
- **Read-Only**: `docs/vision.md`, `README.md`, `promptops/delivery/prod-target.yaml`

#### 3. Implementation Spec
- **Policy Architecture**: Delivery targets define declarative configurations. The delivery worker (`.github/workflows/deliver.yml`) will need to be capable of parsing these new types and executing the corresponding sync logic.
- **Workflow Design**: None (Workflow updates belong to the Executor, but the Executor will need to update `.github/workflows/deliver.yml` to handle `oci` and `npm` delivery types).
- **CODEOWNERS Patterns**: The new files in `promptops/delivery/` will naturally fall under the existing `promptops/delivery/ @apastra/governance-admins` ownership.
- **Promotion Record Format**: No changes.
- **Delivery Target Format**: None
- **Dependencies**: None.

#### 4. Test Plan
- **Verification**: cat .github/CODEOWNERS
- **Success Criteria**: The `.sys/plans/2026-03-15-GOVERNANCE-DeliveryTargets.md` file is created correctly and follows the required template.
- **Edge Cases**: None.
