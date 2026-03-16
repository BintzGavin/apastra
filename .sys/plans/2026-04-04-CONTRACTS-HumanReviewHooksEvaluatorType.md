#### 1. Context & Goal
- **Objective**: Add `human` as an evaluator type to the `evaluator.schema.json` to support human review hooks.
- **Trigger**: `docs/vision.md` explicitly defines `Evaluator` as "Scoring definition: deterministic checks, schema validation, rubric/judge config, or human review hooks." However, the current `evaluator.schema.json` only supports `"deterministic"`, `"schema"`, and `"judge"`.
- **Impact**: This unlocks the ability to define evaluators that pause for or incorporate human grading/review, ensuring the schema fully aligns with the vision document's noun definitions.

#### 2. File Inventory
- **Create**: None.
- **Modify**: `promptops/schemas/evaluator.schema.json`.
- **Read-Only**: `docs/vision.md`.

#### 3. Implementation Spec
- **Schema Architecture**: Add the string `"human"` to the `enum` array for the `type` property in `promptops/schemas/evaluator.schema.json`.
- **Content Digest Convention**: N/A
- **Pseudo-Code**:
  - Update the enum definition in the `evaluator.schema.json` file.
- **Public Contract Changes**: The `evaluator.schema.json` will allow `"human"` as a valid evaluator type.
- **Dependencies**: None.

#### 4. Test Plan
- **Verification**: Run `cat promptops/schemas/evaluator.schema.json | grep '"human"'` to verify the new type is added to the schema.
- **Success Criteria**: The output includes the `"human"` type in the enum.
- **Edge Cases**: Ensure existing tests for valid evaluators (e.g. `deterministic`) still pass.
