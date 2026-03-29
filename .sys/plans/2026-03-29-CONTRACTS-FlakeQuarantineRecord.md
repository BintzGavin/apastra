#### 1. Context & Goal
- **Objective**: Create a JSON Schema and validator for a flake quarantine record to formally track and quarantine flaky evaluation cases.
- **Trigger**: docs/vision.md under "Sample size, variance, and flakiness" explicitly requires the system to "Quarantine flaky cases and track their flake rate; do not let flakiness silently pass as random noise."
- **Impact**: This unlocks the ability for EVALUATION and RUNTIME domains to gracefully skip or specially handle flaky cases during benchmark suites, and allows GOVERNANCE to track the health of test suites over time.

#### 2. File Inventory
- **Create**:
  - promptops/schemas/flake-quarantine-record.schema.json
  - promptops/validators/validate-flake-quarantine-record.sh
- **Modify**: None
- **Read-Only**: docs/vision.md, README.md

#### 3. Implementation Spec
- **Schema Architecture**: A JSON Schema (draft-07) defining the structure of a flake quarantine record.
  - Required fields: record_id, case_id, suite_id, flake_rate (number between 0 and 1), status (enum: quarantined, monitoring, resolved), quarantine_date (date-time).
  - Optional fields: reason (string), resolved_date (date-time), metadata (object).
- **Content Digest Convention**: N/A for this mutable/append-only record, but can optionally include a digest field if canonicalized.
- **Pseudo-Code**:
  - validate-flake-quarantine-record.sh will run ajv validate -s promptops/schemas/flake-quarantine-record.schema.json -d <input_file> --spec=draft2020 --strict=false
- **Public Contract Changes**: Exports https://promptops.apastra.com/schemas/flake-quarantine-record.schema.json
- **Dependencies**: None.

#### 4. Test Plan
- **Verification**: Run promptops/validators/validate-flake-quarantine-record.sh against a valid mock JSON record.
- **Success Criteria**: The validator exits with status 0, confirming the JSON matches the schema.
- **Edge Cases**: Malformed inputs (e.g., flake_rate > 1.0, missing case_id, invalid date-time format) should be rejected by the validator.
