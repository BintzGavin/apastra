#### 1. Context & Goal
- **Objective**: Create a schema and validator for flake quarantine records.
- **Trigger**: docs/vision.md explicitly states the need to "Quarantine flaky cases and track their flake rate; do not let flakiness silently pass as 'random noise'."
- **Impact**: Enables the EVALUATION and GOVERNANCE domains to correctly flag, track, and manage flaky test cases to prevent false confidence.

#### 2. File Inventory
- **Create**:
  - promptops/schemas/flake-quarantine-record.schema.json
  - promptops/validators/validate-flake-quarantine-record.sh
- **Modify**: None
- **Read-Only**: None

#### 3. Implementation Spec
- **Schema Architecture**:
  - $schema: "http://json-schema.org/draft-07/schema"
  - id: Stable identifier for the quarantine record.
  - case_id: The ID of the dataset case being quarantined.
  - suite_id: The ID of the suite where the case flakes.
  - evaluator_id: The evaluator that produced the flaky result.
  - flake_rate: A number representing the observed flake rate.
  - timestamp: The timestamp when the case was quarantined.
  - reason: Explanation of why the case was quarantined.
  - status: The current status of the quarantine (e.g., active, resolved).
- **Content Digest Convention**: N/A
- **Pseudo-Code**:
  - The validator script will use ajv to validate the input JSON against the schema.
- **Public Contract Changes**: Exports apastra-flake-quarantine-record-v1.
- **Dependencies**: None.

#### 4. Test Plan
- **Verification**: Run ajv validate -s promptops/schemas/flake-quarantine-record.schema.json -d <target_file>
- **Success Criteria**: ajv exits with code 0 and prints no errors for a valid JSON.
- **Edge Cases**: Missing required fields or invalid data types should cause ajv to exit with a non-zero code.
