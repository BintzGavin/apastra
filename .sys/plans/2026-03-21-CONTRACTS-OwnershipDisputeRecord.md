#### 1. Context & Goal
- **Objective**: Create a JSON Schema and validation script for an ownership dispute record.
- **Trigger**: `docs/vision.md` explicitly mandates governance policies for "ownership disputes", but no formal machine-readable schema currently exists in the registry to support this workflow.
- **Impact**: Enables the GOVERNANCE domain to programmatically create, manage, and validate ownership disputes, ensuring a reproducible and transparent moderation lifecycle.

#### 2. File Inventory
- **Create**:
  - `promptops/schemas/ownership-dispute-record.schema.json`: JSON schema defining the structure of an ownership dispute record.
  - `promptops/validators/validate-ownership-dispute-record.sh`: Bash script to validate a dispute record against its JSON schema.
- **Modify**: None

#### 3. Implementation Spec
- **Data Schema**: A JSON Schema defining an object. Required properties: `dispute_id` (string), `package_name` (string, the canonical name in dispute), `complainant_id` (string), `timestamp` (string, date-time format), `claim_reason` (string), and `status` (string enum: "open", "under_review", "resolved"). Optional properties: `evidence_links` (array of strings), `resolution_notes` (string).
- **Content Digest Convention**: As an append-only governance record, it relies on standard canonical JSON structure; if hashed, it should follow the SHA-256 standard defined in `digest-convention.md`.
- **Pseudo-Code**:
  1. Define the complete schema properties, types, and required fields in `ownership-dispute-record.schema.json`.
  2. Implement `validate-ownership-dispute-record.sh` to use `ajv validate -s promptops/schemas/ownership-dispute-record.schema.json -d <target-file>`.
- **Public Contract Changes**: Exports the `ownership-dispute-record.schema.json` and its stable schema ID for external consumption by moderation APIs and GOVERNANCE workflows.
- **Dependencies**: Depends on existing basic JSON schema formatting. No cross-domain blockers before execution.
