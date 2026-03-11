#### 1. Context & Goal
- **Objective**: Create schema definition for baseline references to unblock Evaluation.
- **Trigger**: Missing baseline schema blocks the Evaluation regression gating engine; README.md defines baseline as a named reference run/digest for regression comparison.
- **Impact**: Unblocks the EVALUATION regression engine, allowing GOVERNANCE regression policies to reference known immutable run artifacts via digest for comparison.

#### 2. File Inventory
- **Create**: `promptops/schemas/baseline.schema.json` (JSON Schema for baseline reference)
- **Create**: `promptops/validators/validate-baseline.sh` (Validation script for baseline schema)
- **Modify**: None
- **Read-Only**: `promptops/schemas/run-artifact.schema.json`

#### 3. Implementation Spec
- **Schema Architecture**: JSON Schema format. Required fields: `baseline_id` (string), `run_digest` (string), `created_at` (string, datetime format). Optional fields include `metadata` (object) and `description` (string).
- **Content Digest Convention**: SHA-256 of canonical JSON. Computed using `jq -cSM .` and prepending `sha256:`.
- **Pseudo-Code**: Validate the JSON payload against baseline.schema.json. If invalid, reject the reference.
- **Public Contract Changes**: Exports schema ID `apastra-baseline-v1`.
- **Dependencies**: None.

#### 4. Test Plan
- **Verification**:
```bash
echo '{"baseline_id": "prod-current", "run_digest": "sha256:123", "created_at": "2026-03-11T00:00:00Z"}' > test-fixtures/valid-baseline.json
npx ajv-cli validate -s promptops/schemas/baseline.schema.json -d test-fixtures/valid-baseline.json --spec=draft2020 --strict=false
```
- **Success Criteria**:
```bash
[ $? -eq 0 ]
```
- **Edge Cases**:
```bash
echo '{"baseline_id": "prod-current", "created_at": "2026-03-11T00:00:00Z"}' > test-fixtures/missing-digest.json
npx ajv-cli validate -s promptops/schemas/baseline.schema.json -d test-fixtures/missing-digest.json --spec=draft2020 --strict=false
[ $? -ne 0 ]
rm -f test-fixtures/valid-baseline.json test-fixtures/missing-digest.json
```