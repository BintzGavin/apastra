#### 1. Context & Goal
- **Objective**: Define the baseline establishment workflow to explicitly record immutable baselines.
- **Trigger**: The README.md requires baselines to be set explicitly as immutable anchors for regression comparison, but currently only the directory structure `derived-index/baselines/` exists.
- **Impact**: Unlocks the ability for EVALUATION's regression engine to perform policy-evaluated candidate vs. baseline comparisons, which GOVERNANCE relies on for required status checks.

#### 2. File Inventory
- **Create**: A new Python script in `promptops/runs/` to establish and record baselines.
- **Modify**: None.
- **Read-Only**: `README.md`, `promptops/schemas/baseline.schema.json`, `promptops/schemas/run-artifact.schema.json`

#### 3. Implementation Spec
- **Harness Architecture**: N/A
- **Run Request Format**: N/A
- **Run Artifact Format**: The baseline establishment tool must read an existing run artifact to verify its existence and scorecard before establishing it as a baseline.
- **Pseudo-Code**:
  - Parse arguments for suite ID, run digest, and output directory.
  - Verify that the run artifact corresponding to the run digest exists and contains a valid scorecard.
  - Generate a baseline object matching `baseline.schema.json` (including `baseline_id`, `run_digest`, and `created_at`).
  - Write the JSON to the baseline directory.
- **Baseline and Regression Flow**: As noted in the journal, the first run of any suite implicitly becomes the initial candidate or requires a manual bootstrap run using this tool. Once set, the baseline is immutable and regression comparisons always read this pinned baseline digest.
- **Dependencies**: Depends on CONTRACTS `promptops/schemas/baseline.schema.json` and `promptops/schemas/run-artifact.schema.json`.

#### 4. Test Plan
- **Verification**:
  ```bash
  mkdir -p test-fixtures/baselines
  echo '{"baseline_id": "test-suite", "run_digest": "sha256:dummy", "created_at": "2024-01-01T00:00:00Z"}' > test-fixtures/baselines/test-suite.json
  npx --yes ajv-cli validate -s promptops/schemas/baseline.schema.json -d test-fixtures/baselines/test-suite.json --spec=draft2020 --strict=false -c ajv-formats
  ```
- **Success Criteria**:
  ```bash
  npx --yes ajv-cli validate -s promptops/schemas/baseline.schema.json -d test-fixtures/baselines/test-suite.json --spec=draft2020 --strict=false -c ajv-formats && echo "Baseline JSON is valid"
  ```
- **Edge Cases**:
  ```bash
  echo '{"baseline_id": "test-suite"}' > test-fixtures/baselines/invalid.json
  npx --yes ajv-cli validate -s promptops/schemas/baseline.schema.json -d test-fixtures/baselines/invalid.json --spec=draft2020 --strict=false -c ajv-formats || echo "Validation failed correctly for missing fields"
  rm -f test-fixtures/baselines/test-suite.json test-fixtures/baselines/invalid.json
  rmdir test-fixtures/baselines
  ```
