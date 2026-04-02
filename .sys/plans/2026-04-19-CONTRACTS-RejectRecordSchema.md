#### 1. Context & Goal
- **Objective**: Define the schema for `reject-record`.
- **Trigger**: The docs/vision.md flow chart identifies "Reject record + reasons" in the moderation pipeline. This schema is needed to track rejected prompt package submissions.
- **Impact**: Enables the GOVERNANCE domain to programmatically record and act upon rejected submissions.

#### 2. File Inventory
- **Create**: `promptops/schemas/reject-record.schema.json`
- **Create**: `promptops/validators/validate-reject-record.sh`
- **Modify**: `docs/status/CONTRACTS.md`
- **Modify**: `docs/progress/CONTRACTS.md`
- **Read-Only**: []

#### 3. Implementation Spec
- **Schema Architecture**: A JSON Schema definition representing a Reject Record. Fields should include `record_id` (string), `submission_id` (string), `package_digest` (string, sha256 pattern), `reasons` (array of strings), `moderator_id` (string), and `timestamp` (date-time).
- **Content Digest Convention**: N/A for schema definition.
- **Pseudo-Code**:
  - Create the JSON Schema file enforcing required fields.
  - Create the validation shell script to validate against the schema using `ajv-cli`.
- **Public Contract Changes**: Exports the `reject-record` schema ID.
- **Dependencies**: None

#### 4. Test Plan
- **Verification**: `npx ajv-cli validate -s promptops/schemas/reject-record.schema.json -d <valid-fixture>`
- **Success Criteria**: Validation succeeds for compliant fixtures and fails for non-compliant ones.
- **Edge Cases**: Missing reasons or malformed digests should fail validation.
