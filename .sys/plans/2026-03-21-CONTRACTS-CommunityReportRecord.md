#### 1. Context & Goal
- **Objective**: Create a JSON Schema and validation script for a community report record.
- **Trigger**: `docs/vision.md` explicitly mandates "community reporting" as part of the moderation process, but no formal machine-readable schema currently exists in the registry to support this workflow.
- **Impact**: Enables the GOVERNANCE domain to programmatically process, track, and validate community reports regarding prompt packages or models, allowing for an actionable moderation queue.

#### 2. File Inventory
- **Create**:
  - `promptops/schemas/community-report-record.schema.json`: JSON schema defining the structure of a community report.
  - `promptops/validators/validate-community-report-record.sh`: Bash script to validate a community report record against its JSON schema.
- **Modify**: None

#### 3. Implementation Spec
- **Data Schema**: A JSON Schema defining an object. Required properties: `report_id` (string), `target_package_name` (string, the canonical name being reported), `reporter_id` (string), `timestamp` (string, date-time format), `reason_category` (string enum: "malware", "hate_speech", "pii_leak", "spam", "other"), and `status` (string enum: "open", "under_review", "resolved"). Optional properties: `evidence_links` (array of strings), `detailed_description` (string).
- **Content Digest Convention**: As an append-only governance record, it relies on standard canonical JSON structure; if hashed, it should follow the SHA-256 standard defined in `digest-convention.md`.
- **Pseudo-Code**:
  1. Define the complete schema properties, types, and required fields in `community-report-record.schema.json`.
  2. Implement `validate-community-report-record.sh` to use `ajv validate -s promptops/schemas/community-report-record.schema.json -d <target-file>`.
- **Public Contract Changes**: Exports the `community-report-record.schema.json` and its stable schema ID for external consumption by moderation APIs and GOVERNANCE workflows.
- **Dependencies**: Depends on existing basic JSON schema formatting. No cross-domain blockers before execution.
