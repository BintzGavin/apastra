#### 1. Context & Goal
- **Objective**: Provide an initial "Quick Eval" instance file spec for `promptops/evals/`.
- **Trigger**: `docs/vision.md` defines a "Quick eval mode" with a combined file format for rapid iteration, and the schema (`quick-eval.schema.json`) was created, but no initial instance file exists to serve as an example for evaluation harnesses.
- **Impact**: Enables the evaluation and runtime processes to run quick evals by providing a concrete example instance that matches `quick-eval.schema.json`.

#### 2. File Inventory
- **Create**: `promptops/evals/my-eval.yaml` (Initial instance of a quick eval file)
- **Modify**: None
- **Read-Only**: `docs/vision.md`, `promptops/schemas/quick-eval.schema.json`

#### 3. Implementation Spec
- **Schema Architecture**: A YAML file matching `quick-eval.schema.json` containing: `id` (string), `prompt` (string template), `cases` (array of objects with `case_id`, `inputs`, and `assert`), and optionally `thresholds`.
- **Content Digest Convention**: Standard conventions applying to dataset and prompt instances.
- **Pseudo-Code**:
  - Define `id: summarize-quick`.
  - Define `prompt: "Summarize the following text in {{max_length}} or fewer words: {{text}}"`.
  - Add at least one case with a `case_id` (e.g. `short-article`), `inputs` (`text` and `max_length`), and an `assert` list (e.g. `type: icontains`, `value: "fox"`).
  - Add `thresholds` with a `pass_rate` of `1.0`.
- **Public Contract Changes**: No schema modifications; just providing a concrete valid instance.
- **Dependencies**: None.

#### 4. Test Plan
- **Verification**: Run `bash promptops/validators/validate-quick-eval.sh promptops/evals/my-eval.yaml`
- **Success Criteria**: The validation script returns an exit code of 0.
- **Edge Cases**: Missing `id`, `prompt`, or `cases` should be rejected by the schema.
