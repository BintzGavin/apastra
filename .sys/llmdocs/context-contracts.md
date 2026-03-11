# Context: CONTRACTS

## Section A: Schema Inventory
- **ID:** `apastra-run-request-v1`
  - **Version:** 0.9.0
  - **Description:** Schema for a minimal BYO harness run request.
- **ID:** `apastra-run-artifact-v1`
  - **Version:** 0.9.0
  - **Description:** Schema for a minimal BYO harness run artifact output.
- **ID:** `https://promptops.apastra.com/schemas/prompt-spec.schema.json`
  - **Version:** 0.4.0
  - **Description:** Source-of-truth prompt definition with a stable ID, variable schema, output contract, and metadata.
- **ID:** `https://promptops.apastra.com/schemas/dataset-manifest.schema.json`
  - **Version:** 0.4.0
  - **Description:** Schema for a dataset manifest, defining identity, version, schema version, digest, and provenance.
- **ID:** `https://promptops.apastra.com/schemas/dataset-case.schema.json`
  - **Version:** 0.4.0
  - **Description:** Schema defining a single line of a JSONL dataset for evaluating prompt tests.
- **ID:** `https://promptops.apastra.com/schemas/evaluator.schema.json`
  - **Version:** 0.4.0
  - **Description:** Scoring definition (deterministic checks, schema validation, rubric/judge config).
- **ID:** `https://apastra.com/schemas/promptops/suite.schema.json`
  - **Version:** 0.5.0
  - **Description:** Benchmark suite declaring datasets, evaluators, model/provider matrix, trials, budgets, and thresholds.
- **ID:** `https://apastra.com/schemas/promptops/consumption-manifest.schema.json`
  - **Version:** 0.7.0
  - **Description:** Schema for the apastra PromptOps consumption manifest.
- **ID:** `https://apastra.com/schemas/harness-adapter.schema.json`
  - **Version:** 0.8.0
  - **Description:** JSON Schema and validation script for `harness-adapter`.

## Section B: Validator Inventory
- **Validator:** `validate-run-request.sh`
  - **Invocation Syntax:** `./promptops/validators/validate-run-request.sh <run-request.json>`
  - **Validates:** JSON files against the `run-request.schema.json` schema.
- **Validator:** `validate-run-artifact.sh`
  - **Invocation Syntax:** `./promptops/validators/validate-run-artifact.sh <run-artifact.json>`
  - **Validates:** JSON files against the `run-artifact.schema.json` schema.
- **Validator:** `validate-prompt-spec.sh`
  - **Invocation Syntax:** `./promptops/validators/validate-prompt-spec.sh <prompt-spec.json|yaml>`
  - **Validates:** JSON or YAML files against the `prompt-spec.schema.json` schema.
- **Validator:** `validate-dataset.sh`
  - **Invocation Syntax:** `./promptops/validators/validate-dataset.sh <manifest.json|yaml> <cases.jsonl>`
  - **Validates:** Dataset manifest and test cases JSONL file against their respective schemas.
- **Validator:** `validate-evaluator.sh`
  - **Invocation Syntax:** `./promptops/validators/validate-evaluator.sh <evaluator-spec.json|yaml>`
  - **Validates:** JSON or YAML files against the `evaluator.schema.json` schema.
- **Validator:** `validate-suite.sh`
  - **Invocation Syntax:** `./promptops/validators/validate-suite.sh <suite.json|yaml>`
  - **Validates:** JSON or YAML files against the `suite.schema.json` schema.
- **Validator:** `validate-consumption-manifest.sh`
  - **Invocation Syntax:** `./promptops/validators/validate-consumption-manifest.sh <consumption-manifest.json|yaml>`
  - **Validates:** JSON or YAML files against the `consumption-manifest.schema.json` schema.
- **Validator:** `validate-harness-adapter.sh`
  - **Invocation Syntax:** `./promptops/validators/validate-harness-adapter.sh <harness-adapter.json|yaml>`
  - **Validates:** JSON or YAML files against the `harness-adapter.schema.json` schema.

## Section C: Source File Conventions
- **Prompts:**
  - Naming: `prompt.yaml` or `prompt.json`
  - Structure: Lives in `promptops/prompts/<id>/`
  - Required fields: `id` (string), `variables` (object), `template` (string, object, array).
- **Datasets:**
  - Naming: `manifest.json` or `manifest.yaml` and `cases.jsonl`
  - Structure: Lives in `promptops/datasets/<dataset-id>/`
  - Required fields in manifest: `id`, `version`, `schema_version`, `digest`
  - Required fields in case: `case_id`, `inputs`
- **Evaluators:**
  - Naming: `evaluator.yaml` or `evaluator.json`
  - Structure: Lives in `promptops/evaluators/<evaluator-id>/`
  - Required fields: `id` (string), `type` (string: "deterministic", "schema", "judge"), `metrics` (array of strings).
- **Suites:**
  - Naming: `suite.yaml` or `suite.json`
  - Structure: Lives in `promptops/suites/<suite-id>/`
  - Required fields: `id` (string), `name` (string), `datasets` (array), `evaluators` (array), `model_matrix` (array).

## Section D: Digest Convention
- Computed across the canonical representation of the file.
- YAML files are converted to JSON and canonicalized.
- JSON files are canonicalized with sorted keys and insignificant whitespace removed (e.g. `jq -cSM .`).
- JSONL files are canonicalized line by line and joined with newlines.
- The output format is `sha256:<hex>`.
- For dataset cases, the digest is held in the `digest` field of the dataset manifest, which is computed across the `cases.jsonl` file.

## Section E: Integration Points
- **RUNTIME:** Reads manifests schema, dataset manifest schema.
- **EVALUATION:** Reads run request schema, dataset schema.
- **GOVERNANCE:** Reads policy schema.