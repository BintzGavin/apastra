#### 1. Context & Goal
- **Objective**: Create the JSON Schema and validator for comparison scorecards.
- **Trigger**: docs/vision.md proposes a multi-model comparison feature ("Generate a comparison scorecard with per-model breakdowns and a cost/quality/latency tradeoff surface").
- **Impact**: Unlocks the ability for RUNTIME and EVALUATION to generate multi-model comparisons.

#### 2. File Inventory
- **Create**:
  - promptops/schemas/comparison-scorecard.schema.json
  - promptops/validators/validate-comparison-scorecard.sh
- **Modify**: []
- **Read-Only**: []

#### 3. Implementation Spec
- **Schema Architecture**:
  - format: JSON Schema (Draft-07)
  - root type: object
  - properties: run_request_ref, models (array of scorecards), tradeoffs (cost, quality, latency comparisons)
- **Content Digest Convention**: N/A for comparison scorecard file.
- **Pseudo-Code**:
  - validate-comparison-scorecard.sh will invoke ajv to validate the comparison scorecard.
- **Public Contract Changes**: Exports apastra-comparison-scorecard-v1.
- **Dependencies**: None.

#### 4. Test Plan
- **Verification**: ajv validate -s promptops/schemas/comparison-scorecard.schema.json -d test-fixtures/valid-comparison-scorecard.json
- **Success Criteria**: A valid comparison scorecard passes schema validation and a malformed file correctly emits schema errors.
- **Edge Cases**: Missing models array, missing required tradeoff comparisons.
