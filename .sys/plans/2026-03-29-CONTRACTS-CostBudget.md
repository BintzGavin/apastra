#### 1. Context & Goal
- **Objective**: Update suite schemas to use `cost_budget` instead of `cost`.
- **Trigger**: `docs/vision.md` explicitly states "A `cost_budget` field on suites should hard-stop runs that exceed a dollar threshold."
- **Impact**: Ensures that run harnesses correctly interpret the budget field as a hard-stop limit, standardizing cost tracking across all suites.

#### 2. File Inventory
- **Create**: None
- **Modify**:
  - `promptops/schemas/suite.schema.json` (Rename `cost` to `cost_budget` in `budgets` object)
  - `promptops/schemas/canary-suite.schema.json` (Rename `cost` to `cost_budget` in `budgets` object)
- **Read-Only**:
  - `promptops/schemas/run-request.schema.json`

#### 3. Implementation Spec
- **Schema Architecture**: The `cost` field inside the `budgets` object in `suite.schema.json` and `canary-suite.schema.json` will be renamed to `cost_budget`.
- **Content Digest Convention**: No changes to digest convention.
- **Pseudo-Code**:
  ```json
  "budgets": {
    "type": "object",
    "properties": {
      "cost_budget": {
        "type": "number",
        "description": "Maximum allowed cost in dollars."
      }
    }
  }
  ```
- **Public Contract Changes**: `cost` property in `budgets` is now `cost_budget`.
- **Dependencies**: None.

#### 4. Test Plan
- **Verification**: `ajv validate -s promptops/schemas/suite.schema.json -d <test-fixture.json>` and `ajv validate -s promptops/schemas/canary-suite.schema.json -d <test-fixture.json>`
- **Success Criteria**: Validation passes for suites using `cost_budget` and fails for missing required fields (if any).
- **Edge Cases**: Malformed inputs for `cost_budget` (e.g., negative numbers, strings) should be rejected.
