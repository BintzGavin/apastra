#### 1. Context & Goal
- **Objective**: Create a validator script for the prompt-optimization-report schema.
- **Trigger**: The schema for `prompt-optimization-report` exists, but its corresponding validator script is missing, which is a gap in the validation requirements.
- **Impact**: Unlocks the ability for the system or agents to automatically validate prompt optimization reports against their schema, ensuring data integrity.

#### 2. File Inventory
- **Create**:
  - `promptops/validators/validate-prompt-optimization-report.sh`
- **Modify**: []
- **Read-Only**:
  - `promptops/schemas/prompt-optimization-report.schema.json`

#### 3. Implementation Spec
- **Schema Architecture**: The validator will use `ajv` to validate input JSON files against the existing `promptops/schemas/prompt-optimization-report.schema.json` schema.
- **Content Digest Convention**: N/A for this task.
- **Pseudo-Code**:
  1. Check if exactly one argument (the path to the JSON file) is provided. If not, print usage and exit.
  2. Run `ajv validate` with the `-c ajv-formats` option, using `promptops/schemas/prompt-optimization-report.schema.json` as the schema and the provided argument as the data file.
  3. If `ajv validate` succeeds, print "Validation succeeded" and exit with 0.
  4. If `ajv validate` fails, print "Validation failed" and exit with 1.
- **Public Contract Changes**: None.
- **Dependencies**: None.

#### 4. Test Plan
- **Verification**: Run `ajv validate -c ajv-formats -s promptops/schemas/prompt-optimization-report.schema.json -d test-fixtures/valid-prompt-optimization-report.json` using the newly created script.
- **Success Criteria**: The script outputs "Validation succeeded" and exits with status code 0.
