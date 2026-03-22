#### 1. Context & Goal
- **Objective**: Create the Emergency Takedown Decision schema and validation script.
- **Trigger**: `docs/vision.md` explicitly defines "Emergency takedown decisions" as a human checkpoint under the public registry moderation flow. A distinct schema is needed to formally capture this specific action.
- **Impact**: Enables the GOVERNANCE domain to implement procedures for emergency takedowns using a formal schema, preventing state hallucination.

#### 2. File Inventory
- **Create**:
  - `promptops/schemas/emergency-takedown-decision.schema.json`: JSON Schema for emergency takedown decisions.
  - `promptops/validators/validate-emergency-takedown-decision.sh`: Validation script for the schema.
- **Modify**:
  - `docs/status/CONTRACTS.md`: Advance version and log completion.
  - `docs/progress/CONTRACTS.md`: Log the completed task under the new version.
  - `.sys/llmdocs/context-contracts.md`: Register the new schema and validator.
  - `.jules/CONTRACTS.md`: Append a learning entry.
- **Read-Only**:
  - `docs/vision.md`
  - `promptops/schemas/takedown-record.schema.json`

#### 3. Implementation Spec
- **Schema Architecture**:
  - Format: JSON Schema (Draft 2020-12).
  - Required fields: `decision_id`, `package_digest` (SHA-256 pattern) or `target_reference`, `authorizer_id`, `timestamp` (date-time format), `justification`, and `action_taken` (e.g., "immediate_removal").
- **Content Digest Convention**: N/A for this record.
- **Pseudo-Code**:
  - `validate-emergency-takedown-decision.sh` uses `ajv validate -c ajv-formats --spec=draft2020 -s promptops/schemas/emergency-takedown-decision.schema.json -d <target>` on temporary JSON converted files if needed, exiting non-zero on failure.
- **Public Contract Changes**: Exports `https://promptops.apastra.com/schemas/emergency-takedown-decision.schema.json`
- **Dependencies**: None.

#### 4. Test Plan
- **Verification**: Run `ajv validate -c ajv-formats --spec=draft2020 -s promptops/schemas/emergency-takedown-decision.schema.json -d test-fixtures/valid-emergency-takedown.json`
- **Success Criteria**: The validator passes on valid records and fails on invalid records.
- **Edge Cases**: Missing justification, invalid digest format.
