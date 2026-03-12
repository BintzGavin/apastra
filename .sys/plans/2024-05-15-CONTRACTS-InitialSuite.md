#### 1. Context & Goal
- **Objective**: Create the first suite instance `promptops/suites/test-suite.yaml` representing a Benchmark suite.
- **Trigger**: The README.md requires a Benchmark suite declaring datasets, evaluators, model/provider matrix, trials, budgets, and thresholds, and the schema for it is complete but there are no suite instances.
- **Impact**: Unlocks testing and EVALUATION of runs by providing a well-defined suite to execute harnesses against.

#### 2. File Inventory
- **Create**: `promptops/suites/test-suite.yaml` (An initial test suite)
- **Modify**: `docs/status/CONTRACTS.md` (to document the completion of version v0.21.0 InitialSuite)
- **Read-Only**: `promptops/schemas/suite.schema.json`, `promptops/datasets/test-dataset/dataset-manifest.yaml`, `promptops/evaluators/exact-match.yaml`

#### 3. Implementation Spec
- **Schema Architecture**:
  The `test-suite.yaml` file must conform to `promptops/schemas/suite.schema.json`. It will be a YAML file containing:
  - `id`: "test-suite-v1"
  - `name`: "Test Suite"
  - `description`: "Initial suite for testing evaluator exact-match and dataset test-dataset."
  - `datasets`: ["test-dataset"]
  - `evaluators`: ["exact-match-v1"]
  - `model_matrix`: ["gpt-4o-mini"]
  - `trials`: 1
  - `budgets`:
    `cost`: 1.0
    `time`: 60
  - `thresholds`:
    `exact_match_score`: 0.8
- **Content Digest Convention**: A digest will be computed for `test-suite.yaml` via `promptops/validators/compute-digest.sh` and appended to the file.
- **Pseudo-Code**:
  1. Create `promptops/suites/` directory if missing.
  2. Write `test-suite.yaml`
  3. Compute digest using `promptops/validators/compute-digest.sh promptops/suites/test-suite.yaml`
  4. Validate via `promptops/validators/validate-suite.sh promptops/suites/test-suite.yaml`
- **Public Contract Changes**: No schema changes. Just a new instance.
- **Dependencies**: Depends on the existing prompt, dataset, evaluator instances, and `compute-digest.sh`.

#### 4. Test Plan
- **Verification**: `npx ajv-cli validate -s promptops/schemas/suite.schema.json -d <(yq -o=json promptops/suites/test-suite.yaml) --spec=draft2020 --strict=false -c ajv-formats` (or via `./promptops/validators/validate-suite.sh promptops/suites/test-suite.yaml`)
- **Success Criteria**: The validator outputs that the YAML is valid according to the schema.
- **Edge Cases**: Missing required fields `id`, `name`, `datasets`, `evaluators`, `model_matrix` should fail validation.
