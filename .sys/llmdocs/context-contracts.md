# Context: CONTRACTS

## Section A: Schema Inventory
- **ID:** `https://promptops.apastra.com/schemas/prompt-spec.schema.json`
  - **Version:** 0.3.0
  - **Description:** Source-of-truth prompt definition with a stable ID, variable schema, output contract, and metadata.
- **ID:** `https://promptops.apastra.com/schemas/dataset-manifest.schema.json`
  - **Version:** 0.3.0
  - **Description:** Schema for a dataset manifest, defining identity, version, schema version, digest, and provenance.
- **ID:** `https://promptops.apastra.com/schemas/dataset-case.schema.json`
  - **Version:** 0.3.0
  - **Description:** Schema defining a single line of a JSONL dataset for evaluating prompt tests.

## Section B: Validator Inventory
- **Validator:** `validate-prompt-spec.sh`
  - **Invocation Syntax:** `./promptops/validators/validate-prompt-spec.sh <prompt-spec.json|yaml>`
  - **Validates:** JSON or YAML files against the `prompt-spec.schema.json` schema.
- **Validator:** `validate-dataset.sh`
  - **Invocation Syntax:** `./promptops/validators/validate-dataset.sh <manifest.json|yaml> <cases.jsonl>`
  - **Validates:** Dataset manifest and test cases JSONL file against their respective schemas.

## Section C: Source File Conventions
- **Prompts:**
  - Naming: `prompt.yaml` or `prompt.json`
  - Structure: Lives in `promptops/prompts/<id>/`
  - Required fields: `id` (string), `variables` (object), `template` (string, object, array).
- **Datasets:**
  - Naming: `manifest.json` and `cases.jsonl`
  - Structure: Lives in `promptops/datasets/<dataset-id>/`
  - Required fields in manifest: `id`, `version`, `digest`, `schema_version`
  - Required fields in case: `case_id`, `inputs`

## Section D: Digest Convention
- Computed across the canonicalized JSON of the file.
- Format: `sha256:<hex>`
- For dataset cases, the digest is held in the `digest` field of the dataset manifest, which is computed across the `dataset.jsonl` file.

## Section E: Integration Points
- **RUNTIME:** Reads manifests schema, dataset manifest schema.
- **EVALUATION:** Reads run request schema, dataset schema.
- **GOVERNANCE:** Reads policy schema.
