#### 1. Context & Goal
- **Objective**: Implement a formal governance policy for deprecation notices in the registry.
- **Trigger**: `docs/vision.md` specifically requires the append-only registry metadata store to include "deprecation notices", but the existing `promptops/policies/deprecation.md` is a generic placeholder rather than a formal registry-aligned policy detailing append-only behavior.
- **Impact**: Establishes a concrete, auditable mechanism for marking prompt packages as deprecated via append-only metadata records, ensuring consumers receive reliable programmatic signals about sunsetting assets.

#### 2. File Inventory
- **Create**: None
- **Modify**:
  - `promptops/policies/deprecation.md` (Update the generic placeholder to align with the registry metadata append-only architecture).
- **Read-Only**:
  - `docs/vision.md` (Registry metadata store requirements).
  - `promptops/schemas/deprecation-record.schema.json` (Contract definition for the deprecation record artifact).

#### 3. Implementation Spec
- **Policy Architecture**:
  - Define that deprecation of a prompt package or specific version must be executed by appending an immutable `deprecation-record` to the registry metadata store.
  - The record must reference the exact package name and optionally the specific digest/version being deprecated.
  - The policy dictates a minimum 30-day notice period before any active delivery targets or mirrors cease serving the deprecated artifact.
  - Reversal of a deprecation (un-deprecating) requires appending a new, superseding record rather than deleting the original notice.
- **Workflow Design**: N/A (Policy documentation only).
- **CODEOWNERS Patterns**: Inherits existing `@apastra/governance-admins` ownership over `promptops/policies/`.
- **Promotion Record Format**: N/A
- **Delivery Target Format**: N/A
- **Dependencies**: Depends on the stable format defined in `promptops/schemas/deprecation-record.schema.json`.

#### 4. Test Plan
- **Verification**: Ensure the updated policy file is correctly formatted markdown and accurately references the `deprecation-record` schema.
- **Success Criteria**: `promptops/policies/deprecation.md` is robustly updated to describe the append-only registry record model for deprecations.
- **Edge Cases**: N/A for markdown policies.
