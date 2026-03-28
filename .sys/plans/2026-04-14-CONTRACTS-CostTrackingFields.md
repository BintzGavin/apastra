#### 1. Context & Goal
- **Objective**: Add explicit cost tracking fields to the run manifest and regression report schemas.
- **Trigger**: `docs/vision.md` outlines "First-class cost tracking" as a refinement: "Every run manifest should include total cost (input tokens × price + output tokens × price)" and "Regression reports should include cost delta".
- **Impact**: Unlocks the ability for RUNTIME and EVALUATION to natively track and report on execution costs.

#### 2. File Inventory
- **Create**: []
- **Modify**:
  - `promptops/schemas/run-manifest.schema.json`
  - `promptops/schemas/regression-report.schema.json`
- **Read-Only**: []

#### 3. Implementation Spec
- **Schema Architecture**:
  - `promptops/schemas/run-manifest.schema.json`: Add a `total_cost` property (type `number`, description: "Total cost of the run in dollars (input tokens × price + output tokens × price)").
  - `promptops/schemas/regression-report.schema.json`: Add a `cost_delta` property (type `number`, description: "The difference in total cost between the candidate and the baseline").
- **Content Digest Convention**: N/A for these schema definitions directly, though they describe content digest inputs.
- **Pseudo-Code**: Update the JSON schema properties section with these new fields. Update the corresponding validation test files to ensure they accept the new fields.
- **Public Contract Changes**: No IDs change, but standard schemas will support these new optional fields.
- **Dependencies**: None.

#### 4. Test Plan
- **Verification**: `ajv validate -s promptops/schemas/run-manifest.schema.json` against a fixture with a `total_cost` field, and `ajv validate -s promptops/schemas/regression-report.schema.json` against a fixture with a `cost_delta` field.
- **Success Criteria**: Validation succeeds without error.
- **Edge Cases**: Missing cost fields should remain valid as these represent newly added tracking features but might not apply retroactively to all existing artifacts.
