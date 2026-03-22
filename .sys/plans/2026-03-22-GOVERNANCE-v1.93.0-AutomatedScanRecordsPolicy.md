#### 1. Context & Goal
- **Objective**: Create an execution plan spec to formalize the automated scan records policy.
- **Trigger**: `docs/vision.md` explicitly mandates "automated scanning (schema validation, secrets detection, obvious policy checks)" as part of moderation procedures. This policy formalizes the append-only registry metadata storage requirement.
- **Impact**: Establishes a verifiable, append-only trail for automated scan results, ensuring packages meet baseline security and policy requirements before human review.

#### 2. File Inventory
- **Create**:
  - `promptops/policies/automated-scan-records.md`: Formal policy governing the creation and storage of automated scan records.
- **Modify**: None.
- **Read-Only**:
  - `docs/vision.md` (To reference automated scanning requirements)
  - `promptops/schemas/automated-scan-record.schema.json` (To ensure the policy strictly defines required fields and outcomes)

#### 3. Implementation Spec
- **Policy Architecture**:
  - The policy MUST mandate the creation of an `automated-scan-record` JSON artifact containing `scan_id`, `package_digest`, `timestamp`, `scanner_id`, `scan_type`, and `result`.
  - The policy MUST state that historical scan records MUST NEVER be modified or deleted in-place.
- **Workflow Design**: N/A
- **CODEOWNERS Patterns**: N/A
- **Promotion Record Format**: N/A
- **Delivery Target Format**: N/A
- **Dependencies**: Relies on `promptops/schemas/automated-scan-record.schema.json` from the CONTRACTS domain.

#### 4. Test Plan
- **Verification**: The executor will verify the markdown document is created at `promptops/policies/automated-scan-records.md` and contains the required append-only policy guidelines.
- **Success Criteria**: The `automated-scan-records.md` policy document exists and accurately describes the append-only tracking of automated scan results.
- **Edge Cases**: N/A for markdown policy creation.
