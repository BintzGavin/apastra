#### 1. Context & Goal
- **Objective**: Define the foundational machine-readable schemas for dataset manifests and evaluation cases, along with a validator script.
- **Trigger**: `README.md` requires "Dataset: Versioned evaluation cases (usually JSONL) with content digest and schema." Currently, the CONTRACTS domain is missing schemas for datasets, which are a foundational requirement for Evaluation and Suites.
- **Impact**: Unlocks the EVALUATION domain's ability to structure test cases consistently and the RUNTIME domain's ability to accurately ingest datasets for running evaluation suites.

#### 2. File Inventory
- **Create**:
  - `promptops/schemas/dataset-manifest.schema.json` - JSON Schema defining the identity, version, schema version, digest, and provenance of a dataset.
  - `promptops/schemas/dataset-case.schema.json` - JSON Schema defining the structure of individual evaluation test cases (JSONL format, stable case IDs).
  - `promptops/validators/validate-dataset.sh` - CLI tool to validate dataset manifests (YAML/JSON) and evaluate test cases (JSONL) against their respective schemas.
- **Modify**: None.
- **Read-Only**: `README.md` (for noun definitions and constraints).

#### 3. Implementation Spec
- **Schema Architecture**:
  - `dataset-manifest.schema.json` Format: JSON Schema (Draft 2020-12).
  - `dataset-manifest.schema.json` Required fields:
    - `id` (string): Stable identifier for the dataset.
    - `version` (string): Semantic version or revision of the dataset.
    - `digest` (string): Content digest (e.g., SHA-256) of the associated `dataset.jsonl` file to ensure reproducibility.
    - `schema_version` (string): Version of the dataset case schema used by the JSONL file.
  - `dataset-case.schema.json` Format: JSON Schema (Draft 2020-12) defining a single line of a JSONL dataset.
  - `dataset-case.schema.json` Required fields:
    - `case_id` (string): Stable identifier for the specific test case.
    - `inputs` (object): Map of variable names to values, mapping to the variables required by the prompt spec.
  - `dataset-case.schema.json` Optional fields:
    - `expected_outputs` (object): Map of expected output values (e.g., exact matches, substrings).
    - `metadata` (object): Arbitrary metadata for the specific test case (e.g., tags, difficulty, domain).
- **Content Digest Convention**:
  - The dataset manifest explicitly requires a `digest` field that stores the SHA-256 hash of the canonically formatted `dataset.jsonl` file. The hash must be computed before the manifest is finalized.
- **Pseudo-Code** (Validator):
  ```bash
  # promptops/validators/validate-dataset.sh
  # 1. Take input arguments: path to manifest (YAML/JSON) and path to cases (JSONL).
  # 2. Convert manifest YAML to JSON (if needed).
  # 3. Run ajv-cli against promptops/schemas/dataset-manifest.schema.json with the manifest file.
  # 4. For each line in the cases JSONL file:
  # 5.   Run ajv-cli against promptops/schemas/dataset-case.schema.json.
  # 6. Exit 0 if all validations succeed; exit 1 and print errors on failure.
  ```
- **Public Contract Changes**:
  - Exports new schema IDs: `https://promptops.apastra.com/schemas/dataset-manifest.schema.json` and `https://promptops.apastra.com/schemas/dataset-case.schema.json`.
- **Dependencies**: None. Datasets can be defined independently of prompt specs, though their `inputs` will eventually be verified against prompt spec `variables` by evaluators.

#### 4. Test Plan
- **Verification**:
  - Manifest validation: `npx ajv-cli validate -s promptops/schemas/dataset-manifest.schema.json -d test-fixtures/valid-dataset-manifest.json`
  - Case validation: For a given `test-fixtures/valid-dataset.jsonl`, run `npx ajv-cli validate -s promptops/schemas/dataset-case.schema.json -d <(head -n 1 test-fixtures/valid-dataset.jsonl)` (or write a quick script to test the whole JSONL).
- **Success Criteria**: Validator exits with code 0 for both the valid manifest and all valid case lines.
- **Edge Cases**:
  - Reject manifests missing the `id`, `version`, `digest`, or `schema_version`.
  - Reject case lines missing `case_id` or `inputs`.
  - Handle malformed JSONL files cleanly.