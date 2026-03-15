#### 1. Context & Goal
- **Objective**: Add the missing `provenance` field to the dataset manifest schema and validate assertion types in the dataset case schema.
- **Trigger**: `docs/vision.md` specifies that `dataset_manifest.yaml` must contain `provenance` and that dataset case inline assertions have specific built-in types.
- **Impact**: Enables better reproducibility and supply-chain tracking via provenance. Ensures test cases use valid assertion types, preventing typos.

#### 2. File Inventory
- **Create**: None
- **Modify**: `promptops/schemas/dataset-manifest.schema.json` (add `provenance`), `promptops/schemas/dataset-case.schema.json` (add pattern validation to `assert.type`).
- **Read-Only**: `docs/vision.md`, `promptops/validators/validate-dataset.sh`.

#### 3. Implementation Spec
- **Schema Architecture**:
  - `dataset-manifest.schema.json`: Add an optional `provenance` property of type `object` to track origin.
  - `dataset-case.schema.json`: Add a `pattern` to `assert.items.properties.type` to restrict it to valid base types (`equals`, `contains`, `icontains`, `contains-any`, `contains-all`, `regex`, `starts-with`, `is-json`, `contains-json`, `is-valid-json-schema`, `similar`, `llm-rubric`, `factuality`, `answer-relevance`, `latency`, `cost`) with an optional `not-` prefix. Use the pattern `^(not-)?(equals|contains|icontains|contains-any|contains-all|regex|starts-with|is-json|contains-json|is-valid-json-schema|similar|llm-rubric|factuality|answer-relevance|latency|cost)$`.
- **Content Digest Convention**: Handled the same as other standard schemas.
- **Pseudo-Code**: N/A
- **Public Contract Changes**: `dataset-manifest.schema.json` and `dataset-case.schema.json` updated.
- **Dependencies**: None.

#### 4. Test Plan
- **Verification**: `npx yq . promptops/datasets/test-dataset/dataset-manifest.yaml > tmp-manifest.json && npx ajv-cli validate -s promptops/schemas/dataset-manifest.schema.json -d tmp-manifest.json --spec=draft2020 --strict=false && rm tmp-manifest.json`
- **Success Criteria**: Exit code 0 for valid schemas.
- **Edge Cases**: Validation should fail if `type` in an `assert` block is invalid (e.g., `invalid-type`).