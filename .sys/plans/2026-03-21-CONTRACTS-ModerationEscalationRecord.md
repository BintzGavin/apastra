#### 1. Context & Goal
- **Objective**: Create a JSON schema and validation script for a moderation escalation record.
- **Trigger**: The docs/vision.md file explicitly requires "a human escalation path for high-risk content" as a core moderation procedure (line 659). This missing concept needs a formalized schema so downstream domains can generate and track these decisions without state hallucination.
- **Impact**: Unlocks the GOVERNANCE domain's ability to formally record, review, and process moderation escalations, allowing human moderators to handle high-risk submissions programmatically.

#### 2. File Inventory
- **Create**:
  - `promptops/schemas/moderation-escalation-record.schema.json`: Schema defining the required fields for human moderation escalation.
  - `promptops/validators/validate-moderation-escalation-record.sh`: Shell script using `ajv` to validate escalation records against the schema.
- **Modify**: None
- **Read-Only**:
  - `docs/vision.md`: Source of truth for governance and moderation requirements.
  - `promptops/schemas/moderation-decision-record.schema.json`: Existing moderation record schema for reference.

#### 3. Implementation Spec
- **Schema Architecture**:
  - Format: JSON Schema (Draft 2020-12)
  - Required fields: `escalation_id` (string), `submission_id` (string), `escalated_by` (string), `reason` (string), `timestamp` (date-time format), and `status` (enum: "pending", "reviewed", "dismissed").
  - Additional fields: `reviewer_id` (string, optional), `notes` (string, optional).
- **Content Digest Convention**:
  - Not explicitly required for this schema, though any implementation should treat the overall record as immutable once created.
- **Pseudo-Code**:
  - The `validate-moderation-escalation-record.sh` script should accept a single argument (the JSON file to validate) and execute: `ajv validate -c ajv-formats -s promptops/schemas/moderation-escalation-record.schema.json -d "$1"`
- **Public Contract Changes**:
  - Exported schema ID: `https://promptops.apastra.com/schemas/moderation-escalation-record.schema.json`
- **Dependencies**: None. Can be completed autonomously by the CONTRACTS domain.

#### 4. Test Plan
- **Verification**:
  - Create a temporary valid mock JSON representing a moderation escalation record.
  - Create a temporary invalid mock JSON representing a moderation escalation record (e.g., missing a required field or invalid status enum).
  - Run `./promptops/validators/validate-moderation-escalation-record.sh test_valid.json && ! ./promptops/validators/validate-moderation-escalation-record.sh test_invalid.json`.
  - Remove the temporary mock files.
- **Success Criteria**: The validator succeeds (exit code 0) for the valid payload and fails (non-zero exit code) for the invalid payload.
- **Edge Cases**: Malformed statuses outside the enum options; missing required fields; invalid timestamp formats.
