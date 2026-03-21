#### 1. Context & Goal
- **Objective**: Create a JSON Schema and validation script for a takedown appeal record.
- **Trigger**: The docs/vision.md identifies governance and moderation procedures, specifically takedown appeals, as required for a public registry, but there is no takedown appeal schema in promptops/schemas/.
- **Impact**: Unlocks the GOVERNANCE domain's ability to formally process and track appeals to moderation takedowns.

#### 2. File Inventory
- **Create**:
  - `promptops/schemas/takedown-appeal-record.schema.json`: JSON schema for a takedown appeal record.
  - `promptops/validators/validate-takedown-appeal-record.sh`: Bash script to validate a takedown appeal record against its schema.
- **Modify**: None

#### 3. Implementation Spec
- **Data Schema**: A JSON Schema defining an object with required fields like `appeal_id`, `takedown_record_id` (reference to the original takedown), `appellant_id`, `reasoning` (string), and `status` (enum: pending, approved, rejected). Optional fields could include `evidence_links`.
- **Content Digest Convention**: A content digest is not strictly required for the appeal record itself unless it's bundled as part of a larger verifiable artifact, but if needed, it should follow the canonical JSON SHA-256 convention.
- **Pseudo-Code**:
  1.  Define the JSON Schema structure with required and optional properties.
  2.  Write a shell script that uses `ajv` to validate an input JSON file against `promptops/schemas/takedown-appeal-record.schema.json`.
- **Public Contract Changes**: Exports the `takedown-appeal-record.schema.json` format for use by moderation and governance tooling.
- **Dependencies**: None.
