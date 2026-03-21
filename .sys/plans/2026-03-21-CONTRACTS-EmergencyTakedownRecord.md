#### 1. Context & Goal
- **Objective**: Create a JSON schema and validator script for an Emergency Takedown Record.
- **Trigger**: The docs/vision.md requires "Emergency takedown decisions" as human checkpoints.
- **Impact**: Enables the GOVERNANCE domain to programmatically track, validate, and enforce emergency takedown decisions without hallucinating state.

#### 2. File Inventory
- **Create**:
  - `promptops/schemas/emergency-takedown-record.schema.json`
  - `promptops/validators/validate-emergency-takedown-record.sh`
- **Modify**: None
- **Read-Only**: None

#### 3. Implementation Spec
- **Schema Architecture**: JSON schema defining an emergency takedown record with properties: `decision_id`, `package_digest` (must match SHA-256 format), `authorizer_id`, `reason`, `timestamp` (date-time format), and `justification_for_emergency`. All fields are required.
- **Content Digest Convention**: SHA-256 for `package_digest`.
- **Pseudo-Code**:
  ```bash
  # Validate using ajv against the schema
  TMP_FILE=$(mktemp --suffix=.json)
  python3 -c 'import sys, yaml, json; json.dump(yaml.safe_load(sys.stdin), sys.stdout)' < "$1" > "$TMP_FILE"
  ajv validate -c ajv-formats -s promptops/schemas/emergency-takedown-record.schema.json -d "$TMP_FILE"
  rm -f "$TMP_FILE"
  ```
- **Public Contract Changes**: Exports the schema ID `https://promptops.apastra.com/schemas/emergency-takedown-record.schema.json`
- **Dependencies**: None
