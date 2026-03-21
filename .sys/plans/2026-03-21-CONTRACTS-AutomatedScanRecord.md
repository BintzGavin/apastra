#### 1. Context & Goal
- **Objective**: Create an execution plan spec for the `automated-scan-record.schema.json` and its validator.
- **Trigger**: `docs/vision.md` explicitly mandates "automated scanning (schema validation, secrets detection, obvious policy checks)" as part of the moderation procedures.
- **Impact**: Enables the GOVERNANCE domain to programmatically record and act upon automated scan results, ensuring packages meet baseline security and policy requirements before human review.

#### 2. File Inventory
- **Create**:
  - `promptops/schemas/automated-scan-record.schema.json`: The schema definition for an automated scan record.
  - `promptops/validators/validate-automated-scan-record.sh`: A shell script to validate scan records against the new schema.
- **Modify**: None.

#### 3. Implementation Spec
- **Data Schema**: A JSON Schema defining an automated scan record. Required fields must include `scan_id`, `package_digest` (linking to the package scanned), `timestamp`, `scanner_id` (the tool or service performing the scan), `scan_type` (e.g., `malware`, `secrets`, `schema`, `policy`), and `result` (e.g., `pass`, `fail`, `warn`). Optional fields may include `evidence_links` and `detailed_report`.
- **Content Digest Convention**: N/A for this schema definition, though instances of the record may be hashed by GOVERNANCE.
- **Pseudo-Code**: A validation script (`validate-automated-scan-record.sh`) that uses `ajv validate -s promptops/schemas/automated-scan-record.schema.json -d "$1"` to ensure input JSON records conform to the schema.
- **Public Contract Changes**: Exports the new `automated-scan-record.schema.json`.
- **Dependencies**: None.
