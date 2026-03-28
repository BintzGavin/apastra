#### 1. Context & Goal
- **Objective**: Create JSON Schema and validation script for comparison-scorecard.
- **Trigger**: docs/vision.md requires a "Comparison scorecard" in the expansion nouns to support multi-model evaluation.
- **Impact**: Enables multi-model evaluation scorecards with cost/quality/latency tradeoffs.

#### 2. File Inventory
- **Create**:
  - `promptops/schemas/comparison-scorecard.schema.json`: Schema definition for the comparison scorecard.
  - `promptops/validators/validate-comparison-scorecard.sh`: Shell script to validate the schema against fixtures.
- **Modify**: []
- **Read-Only**: []

#### 3. Implementation Spec
- **Schema Architecture**: JSON Schema defining `id`, `suite_id`, `baselines`, `models`, `metrics`, and comparison tradeoffs.
- **Content Digest Convention**: N/A
- **Pseudo-Code**: Validate using ajv.
- **Public Contract Changes**: Export `comparison-scorecard.schema.json`.
- **Dependencies**: None.

#### 4. Test Plan
- **Verification**: Run `validate-comparison-scorecard.sh`
- **Success Criteria**: Validation script succeeds on a valid test fixture and fails on an invalid one.
- **Edge Cases**: Missing models or metrics in the multi-model comparison.
