#### 1. Context & Goal
- **Objective**: Define schemas for Quick Eval Mode and Inline Assertions.
- **Trigger**: `docs/vision.md` outlines "Inline assertions" on dataset cases to simplify eval rules, and "Quick eval mode" to combine prompts, cases, assertions into a single YAML file (`promptops/evals/my-eval.yaml`).
- **Impact**: Enables EVALUATION to natively parse dataset assertions and standalone eval files, allowing low-friction iteration without full suites.

#### 2. File Inventory
- **Create**: `promptops/schemas/quick-eval.schema.json` (Schema for the combined quick eval YAML), `promptops/validators/validate-quick-eval.sh` (Validator script).
- **Modify**: `promptops/schemas/dataset-case.schema.json` (Add `assert` array property).
- **Read-Only**: `docs/vision.md`.

#### 3. Implementation Spec
- **Schema Architecture**:
  - Update `dataset-case.schema.json` to allow an optional `assert` property (array of objects with `type` and `value` fields).
  - Create `quick-eval.schema.json` as a standalone definition combining `id` (string), `prompt` (string template), `cases` (array of dataset cases with inputs and inline asserts), and `thresholds` (object).
- **Content Digest Convention**: Handled the same as other standard schemas; canonicalization of YAML format before hashing.
- **Pseudo-Code**:
  - `validate-quick-eval.sh`: Use `yq` to convert the target yaml file to json, then use `ajv-cli` to validate against `quick-eval.schema.json`.
- **Public Contract Changes**: New exported schema `quick-eval.schema.json` and updated dataset case interface to include assertions.
- **Dependencies**: EVALUATION domain requires these schema formats to implement the Quick Eval running mode.

#### 4. Test Plan
- **Verification**: Run `bash promptops/validators/validate-quick-eval.sh promptops/evals/test-eval.yaml` after defining an example in `promptops/evals/`.
- **Success Criteria**: The JSON Schema correctly rejects files missing `id` or `cases`, and validates valid structures.
- **Edge Cases**: Malformed inline assertion types, missing threshold objects, incorrect variable types in cases.
