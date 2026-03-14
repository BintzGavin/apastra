#### 1. Context & Goal
- **Objective**: Create the initial quick eval file format.
- **Trigger**: The docs (`docs/vision.md`) define a quick eval mode that allows prompts, cases, and assertions in one file. The schema (`promptops/schemas/quick-eval.schema.json`) was created, but the instance file (`promptops/evals/my-eval.yaml`) is missing.
- **Impact**: Enables rapid iteration without the need to define multiple separate files. RUNTIME and EVALUATION depend on this to correctly parse and run quick evals.

#### 2. File Inventory
- **Create**: `promptops/evals/my-eval.yaml` - Initial quick eval test fixture based on the vision doc.
- **Modify**: None.
- **Read-Only**: `docs/vision.md`, `promptops/schemas/quick-eval.schema.json`

#### 3. Implementation Spec
- **Schema Architecture**: A YAML document conforming to `quick-eval.schema.json`. It includes `id`, `prompt`, `cases` (each with `case_id`, `inputs`, `assert`), and `thresholds`.
- **Content Digest Convention**: Handled externally.
- **Pseudo-Code**:
  - Create the file `promptops/evals/my-eval.yaml` with the following content:
    ```yaml
    id: summarize-quick
    prompt: |
      Summarize the following text in {{max_length}} or fewer words: {{text}}
    cases:
      - case_id: short-article
        inputs:
          text: "The quick brown fox jumps over the lazy dog."
          max_length: "10"
        assert:
          - type: icontains
            value: "fox"
          - type: not-contains
            value: "Lorem ipsum"
      - case_id: empty-input
        inputs:
          text: ""
          max_length: "10"
        assert:
          - type: regex
            value: ".*"
    thresholds:
      pass_rate: 1.0
    ```
- **Public Contract Changes**: None.
- **Dependencies**: None.

#### 4. Test Plan
- **Verification**: Run `./promptops/validators/validate-quick-eval.sh promptops/evals/my-eval.yaml`.
- **Success Criteria**: The script exits 0.
- **Edge Cases**: Missing `id`, `prompt`, or `cases` should fail validation.