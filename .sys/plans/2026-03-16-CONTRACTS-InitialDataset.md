#### 1. Context & Goal
- **Objective**: Create the first dataset instance in the repository under the standard `promptops/datasets/` directory.
- **Trigger**: The README.md requires datasets as the versioned evaluation cases (JSONL) with content digest and schema. While schemas exist (`dataset-manifest.schema.json` and `dataset-case.schema.json`), `promptops/datasets/` is currently missing instances.
- **Impact**: Unlocks the ability for EVALUATION and RUNTIME to process concrete test cases against prompt specs, and serves as the prerequisite for creating Evaluator and Suite instances.

#### 2. File Inventory
- **Create**:
  - `promptops/datasets/test-dataset/dataset-manifest.yaml` - YAML manifest defining the dataset identity, version, schema version, and digest.
  - `promptops/datasets/test-dataset/dataset.jsonl` - JSON Lines file containing the actual test cases.
- **Modify**: None
- **Read-Only**: `promptops/schemas/dataset-manifest.schema.json`, `promptops/schemas/dataset-case.schema.json`, `promptops/validators/compute-digest.sh`

#### 3. Implementation Spec
- **Schema Architecture**:
  - `dataset.jsonl`: A JSON Lines file where each line conforms to `promptops/schemas/dataset-case.schema.json`. It must contain `case_id` and `inputs` objects.
  - `dataset-manifest.yaml`: A YAML file conforming to `promptops/schemas/dataset-manifest.schema.json`. Must contain `id`, `version`, `schema_version`, and a `digest` field.
- **Content Digest Convention**: The manifest's `digest` field must exactly match the output of `promptops/validators/compute-digest.sh promptops/datasets/test-dataset/dataset.jsonl`.
- **Pseudo-Code**: N/A for data files.
- **Public Contract Changes**: Exports the first dataset instance `test-dataset`.
- **Dependencies**: The prompt spec `test-prompt` is available as a reference for expected `inputs`.

#### 4. Test Plan
- **Verification**:
  ```bash
  mkdir -p test-fixtures
  echo '{"case_id": "case-1", "inputs": {"text": "hello"}}' > test-fixtures/dataset.jsonl
  DIGEST=$(promptops/validators/compute-digest.sh test-fixtures/dataset.jsonl)
  cat << MANIFEST > test-fixtures/dataset-manifest.yaml
  id: "test-dataset"
  version: "1.0.0"
  schema_version: "https://promptops.apastra.com/schemas/dataset-case.schema.json"
  digest: "$DIGEST"
  MANIFEST
  promptops/validators/validate-dataset.sh test-fixtures/dataset-manifest.yaml test-fixtures/dataset.jsonl
  rm -rf test-fixtures/dataset*
  ```
- **Success Criteria**: `validate-dataset.sh` returns validation passed (exit code 0).
- **Edge Cases**: Modifying the JSONL file without updating the manifest's digest will cause validation failure.
