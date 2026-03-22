#### 1. Context & Goal
- **Objective**: Create an execution plan spec to formalize the community report records policy.
- **Trigger**: `docs/vision.md` explicitly mandates "community reporting" as part of moderation procedures. This policy formalizes the append-only registry metadata storage requirement.
- **Impact**: Establishes a verifiable, append-only trail for community reports, ensuring packages meet baseline security and policy requirements before human review.

#### 2. File Inventory
- **Create**:
  - `promptops/policies/community-report-records.md`: Formal policy governing the creation and storage of community report records.
- **Modify**: None.
- **Read-Only**:
  - `docs/vision.md` (To reference community reporting requirements)
  - `promptops/schemas/community-report-record.schema.json` (To ensure the policy strictly defines required fields and outcomes)

#### 3. Implementation Spec
- **Policy Architecture**:
  - The policy MUST mandate the creation of a `community-report-record` JSON artifact containing `report_id`, `target_package_name`, `reporter_id`, `timestamp`, `reason_category`, and `status`.
  - The policy MUST state that historical report records MUST NEVER be modified or deleted in-place.
- **Workflow Design**: N/A
- **CODEOWNERS Patterns**: N/A
- **Promotion Record Format**: N/A
- **Delivery Target Format**: N/A
- **Dependencies**: Relies on `promptops/schemas/community-report-record.schema.json` from the CONTRACTS domain.

#### 4. Test Plan
- **Verification**: The executor will verify the markdown document is created at `promptops/policies/community-report-records.md` and contains the required append-only policy guidelines.
- **Success Criteria**: The `community-report-records.md` policy document exists and accurately describes the append-only tracking of community report results.
- **Edge Cases**: N/A for markdown policy creation.
