#### 1. Context & Goal
- **Objective**: Create JSON schema and validator for Audit Reports.
- **Trigger**: `docs/vision.md` explicitly calls for "Audit report" under "Expansion Nouns Requiring Schema" and describes the zero-config first contact Audit skill.
- **Impact**: Enables the RUNTIME domain to output standardized, machine-readable prompt debt audits detailing untested and unversioned prompts.

#### 2. File Inventory
- **Create**:
  - `promptops/schemas/audit-report.schema.json`
  - `promptops/validators/validate-audit-report.sh`
- **Modify**: []
- **Read-Only**: `docs/vision.md`

#### 3. Implementation Spec
- **Schema Architecture**:
  - `$schema`: http://json-schema.org/draft-07/schema#
  - `$id`: https://promptops.com/schemas/audit-report.schema.json
  - `type`: object
  - `properties`:
    - `timestamp`: string (date-time)
    - `scanned_paths`: array of strings
    - `total_prompts`: integer
    - `untested_prompts`: integer
    - `unversioned_prompts`: integer
    - `severity_score`: string (e.g., low, medium, high, critical) or number
    - `findings`: array of objects detailing file paths, issue type, and auto-generated scaffold suggestions
  - `required`: ["timestamp", "scanned_paths", "total_prompts", "severity_score", "findings"]
- **Content Digest Convention**: N/A for audit reports directly, as they are point-in-time runtime outputs, but can be hashed via standard canonical JSON if stored.
- **Pseudo-Code**: Validation scripts will use `ajv validate -s promptops/schemas/audit-report.schema.json -d "$1"`
- **Public Contract Changes**: Exports `https://promptops.com/schemas/audit-report.schema.json`.
- **Dependencies**: None.

#### 4. Test Plan
- **Verification**: Run `promptops/validators/validate-audit-report.sh` against a valid mock JSON representing an audit report.
- **Success Criteria**: Validation script succeeds without errors on a well-formed JSON matching the schema.
- **Edge Cases**: Reject missing required fields or invalid property types.
