#### 1. Context & Goal
- **Objective**: Create a JSON Schema and validation script for `submission-record` to define the append-only artifact structure for package submissions to a public registry.
- **Trigger**: `docs/vision.md` outlines "Submission records" as required append-only artifacts under the single-custodian registry model. `promptops/schemas/` currently lacks this definition.
- **Impact**: Unlocks the ability to validate and process incoming package submissions securely and traceably, acting as a foundational schema for public registry publishing and moderation pipelines.

#### 2. File Inventory
- **Create**:
  - `promptops/schemas/submission-record.schema.json`
  - `promptops/validators/validate-submission-record.sh`
- **Modify**:
  - `docs/status/CONTRACTS.md`
  - `docs/progress/CONTRACTS.md`
- **Read-Only**:
  - `docs/vision.md`
  - `promptops/schemas/digest-convention.md`

#### 3. Implementation Spec
- **Schema Architecture**: JSON Schema defining `submission_id` (string), `package_digest` (string, matching SHA-256 pattern), `publisher_id` (string), `timestamp` (string, date-time format), and optional `metadata`.
- **Content Digest Convention**: Following `digest-convention.md`, any digests referenced must be the SHA-256 hash of canonical JSON.
- **Pseudo-Code**:
  - `npx ajv-cli validate -s promptops/schemas/submission-record.schema.json -d <data>`
- **Public Contract Changes**: Exports `apastra-submission-record-v1` schema.
- **Dependencies**: None.

#### 4. Test Plan
- **Verification**: echo '{"submission_id": "sub-123", "package_digest": "sha256:e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855", "publisher_id": "user-456", "timestamp": "2026-03-15T12:00:00Z"}' > test-valid-submission.json && bash promptops/validators/validate-submission-record.sh test-valid-submission.json
- **Success Criteria**: The script exits with status 0 and outputs "test-valid-submission.json is valid".
- **Edge Cases**: Missing required fields or invalid digest/timestamp formats should be rejected by the schema validation.
