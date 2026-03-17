#### 1. Context & Goal
- **Objective**: Add `version` to evaluator metrics and `scorecard.json` metric definitions.
- **Trigger**: `docs/vision.md` explicitly calls out: "How will you model evaluator evolution and metric versioning to preserve long-term comparability?" and "Scorecard: Normalized metrics summary for a run, including metric definitions and metric versioning." The current schemas do not define versions for metrics in `evaluator.schema.json` and leave `metric_definitions` in `scorecard.schema.json` as un-versioned arbitrary objects.
- **Impact**: Enables the EVALUATION domain to perform verifiable historical comparisons and prevents silent semantic drift in scorecards.

#### 2. File Inventory
- **Create**: None
- **Modify**:
  - `promptops/schemas/evaluator.schema.json`
  - `promptops/schemas/scorecard.schema.json`
- **Read-Only**: `docs/vision.md`, `README.md`

#### 3. Implementation Spec
- **Schema Architecture**:
  - Update `promptops/schemas/evaluator.schema.json`: Add a `metric_versions` object mapping metric names to version strings. It is optional.
  - Update `promptops/schemas/scorecard.schema.json`: The `metric_definitions` field is an object mapping metric names to their definitions. We must update the schema for `metric_definitions`'s `additionalProperties` to be an object that explicitly requires a `version` string property.
- **Content Digest Convention**: N/A
- **Pseudo-Code**:
  - Modify `evaluator.schema.json` properties to include `"metric_versions": { "type": "object", "description": "Mapping of metric names to their semantic versions." }`.
  - Modify `scorecard.schema.json` properties so `metric_definitions` has `"additionalProperties": { "type": "object", "properties": { "version": { "type": "string" }, "description": { "type": "string" } }, "required": ["version"] }`.
- **Public Contract Changes**: Scorecard and Evaluator schemas are updated to enforce versioning.
- **Dependencies**: EVALUATION domain must update `normalize.py` to extract `metric_versions` from evaluator outputs and inject them into the scorecard's `metric_definitions`.

#### 4. Test Plan
- **Verification**: `npx ajv-cli validate -s promptops/schemas/scorecard.schema.json -d test-fixtures/valid-scorecard.json --spec=draft2020 --strict=false`
- **Success Criteria**:
```bash
[ $? -eq 0 ]
```
- **Edge Cases**:
```bash
npx ajv-cli validate -s promptops/schemas/scorecard.schema.json -d test-fixtures/missing-version-scorecard.json --spec=draft2020 --strict=false
[ $? -ne 0 ]
```