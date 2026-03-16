#### 1. Context & Goal
- **Objective**: Create JSON Schemas and validation scripts for `moderation-decision-record`, `deprecation-record`, `takedown-record`, and `mirror-sync-receipt`.
- **Trigger**: `docs/vision.md` outlines "Moderation decision records", "Deprecation and takedown records", and "Mirror sync receipts" as required append-only artifacts under the single-custodian registry model mapping. `promptops/schemas/` currently lacks these definitions.
- **Impact**: Completes the foundational schema coverage required for the public registry publishing, moderation, and mirroring pipelines, unlocking automated enforcement and synchronization.

#### 2. File Inventory
- **Create**:
  - `promptops/schemas/moderation-decision-record.schema.json`
  - `promptops/schemas/deprecation-record.schema.json`
  - `promptops/schemas/takedown-record.schema.json`
  - `promptops/schemas/mirror-sync-receipt.schema.json`
  - `promptops/validators/validate-moderation-decision-record.sh`
  - `promptops/validators/validate-deprecation-record.sh`
  - `promptops/validators/validate-takedown-record.sh`
  - `promptops/validators/validate-mirror-sync-receipt.sh`
- **Modify**: None
- **Read-Only**:
  - `docs/vision.md`

#### 3. Implementation Spec
- **Schema Architecture**:
  - `moderation-decision-record`: JSON Schema defining `decision_id`, `submission_id` or `package_digest`, `decision` (approved/rejected/flagged), `moderator_id`, `timestamp`, and `reason`.
  - `deprecation-record`: JSON Schema defining `deprecation_id`, `package_digest` or `reference`, `timestamp`, `reason`, and optional `replacement_ref`.
  - `takedown-record`: JSON Schema defining `takedown_id`, `package_digest`, `timestamp`, `reason`, and `policy_violation_type`.
  - `mirror-sync-receipt`: JSON Schema defining `receipt_id`, `mirror_id`, `synced_digests` (array of strings), `timestamp`, and `status`.
- **Content Digest Convention**: Following `digest-convention.md`, any digests referenced must be the SHA-256 hash of canonical JSON.
- **Pseudo-Code**:
  - Create the 4 JSON schema files conforming to JSON Schema Draft 2020-12.
  - Create the 4 corresponding validation bash scripts running `npx ajv-cli validate -s <schema> -d "$1" -c ajv-formats`.
- **Public Contract Changes**: Exports schemas for the single-custodian registry public API endpoints.
- **Dependencies**: None.

#### 4. Test Plan
- **Verification**: npx ajv-cli compile -s promptops/schemas/moderation-decision-record.schema.json -c ajv-formats && npx ajv-cli compile -s promptops/schemas/deprecation-record.schema.json -c ajv-formats && npx ajv-cli compile -s promptops/schemas/takedown-record.schema.json -c ajv-formats && npx ajv-cli compile -s promptops/schemas/mirror-sync-receipt.schema.json -c ajv-formats
- **Success Criteria**: All schema compilations succeed without errors.
- **Edge Cases**: Missing required fields or invalid formats should be rejected by the schemas during validation.