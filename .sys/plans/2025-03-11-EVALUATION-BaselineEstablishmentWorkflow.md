#### 1. Context & Goal
- **Objective**: Define the Baseline Establishment Workflow to pin a run artifact digest as a reference for regression comparison.
- **Trigger**: The `README.md` defines a baseline as a "Named reference run/digest for regression comparison" and specifies it is "Stored in `derived-index/baselines/`". The run-request and regression engines depend on baselines to perform comparisons.
- **Impact**: Unlocks the ability to track regressions by providing an immutable anchor against which new candidate run artifacts are compared.

#### 2. File Inventory
- **Create**: A new bash script in `promptops/runs/` to validate and store baselines in `derived-index/baselines/`.
- **Modify**: `docs/status/EVALUATION.md`
- **Read-Only**: `promptops/schemas/baseline.schema.json`, `README.md`

#### 3. Implementation Spec
- **Harness Architecture**: N/A for this step.
- **Run Request Format**: N/A.
- **Run Artifact Format**: N/A.
- **Baseline and Regression Flow**:
  1. The new bash script will take arguments: `<suite_id>`, `<name>`, and `<run_artifact_digest>`.
  2. The script will generate a baseline JSON object containing the inputs and the current UTC timestamp for `created_at`.
  3. The JSON will be validated against `promptops/schemas/baseline.schema.json` using `ajv-cli`.
  4. If valid, the JSON will be saved as a dynamically named JSON file in `derived-index/baselines/`.
  5. The baseline acts as a named pointer to a specific, immutable run artifact. Baselines are established explicitly. The first run of a suite implicitly becomes the initial candidate or requires a manual bootstrap run.
- **Dependencies**:
  - CONTRACTS domain schemas: `promptops/schemas/baseline.schema.json` must be defined and available.

#### 4. Test Plan
- **Verification**:
  ```bash
  # Ensure the derived-index/baselines/ directory exists for testing
  mkdir -p derived-index/baselines/
  # The executor must replace [YOUR_BASELINE_SCRIPT] with the exact path to the script they create
  [YOUR_BASELINE_SCRIPT] test-suite test-baseline sha256:dummy
  ```
- **Success Criteria**:
  ```bash
  # Verify that the script succeeds and the JSON file was created
  [ $? -eq 0 ]
  # Since the exact output filename will be dynamic, we check that at least one file was created in the baselines directory that wasn't there before
  ls derived-index/baselines/ | grep -q "test-suite"
  [ $? -eq 0 ]
  ```
- **Edge Cases**:
  ```bash
  # Missing arguments should fail
  [YOUR_BASELINE_SCRIPT] test-suite test-baseline
  [ $? -ne 0 ]

  # Invalid run artifact digest format
  [YOUR_BASELINE_SCRIPT] test-suite test-baseline invalid_digest
  [ $? -ne 0 ]
  ```