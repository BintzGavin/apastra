#### 1. Context & Goal
- **Objective**: Implement drift detection (canary suites).
- **Trigger**: `docs/vision.md` outlines "Drift detection" as Expansion 2 (P1), requiring canary suites that run on a schedule to catch post-ship quality erosion caused by silent model provider updates.
- **Impact**: Enables post-ship quality monitoring by comparing canary results against production baselines, fulfilling a critical P1 expansion gap.

#### 2. File Inventory
- **Create**: `promptops/runs/drift_detection.sh` (Script to run canary suites and compare with production baselines)
- **Modify**: None
- **Read-Only**: `promptops/schemas/baseline.schema.json`, `docs/vision.md`, `promptops/runs/runner-shim.sh`, `promptops/runs/compare.py`

#### 3. Implementation Spec
- **Harness Architecture**: A new script `drift_detection.sh` will orchestrate the execution of a canary suite via `runner-shim.sh` and then compare the output scorecard against a specified production baseline using `compare.py` or `generate_regression_report.sh`.
- **Run Request Format**: Takes a pre-defined run request for the canary suite.
- **Run Artifact Format**: Emits a `drift_report.json` based on the comparison, highlighting regressions.
- **Pseudo-Code**:
  ```bash
  #!/bin/bash
  # pseudo-code for drift_detection.sh
  CANARY_RUN_REQ=$1
  PROD_BASELINE=$2
  OUT_DIR=$3

  # run canary suite
  ./promptops/runs/runner-shim.sh adapter.yaml $CANARY_RUN_REQ $OUT_DIR

  # compare against baseline
  ./promptops/runs/generate_regression_report.sh $OUT_DIR/scorecard.json $PROD_BASELINE policy.yaml $OUT_DIR/drift_report.json
  ```
- **Baseline and Regression Flow**: Utilizes the existing baseline schema and regression generation scripts to report drift.
- **Dependencies**: Depends on existing execution scripts (`runner-shim.sh`, `generate_regression_report.sh`) and CONTRACTS schemas.

#### 4. Test Plan
- **Verification**: Ensure the script runs successfully given a canary suite run request and a valid production baseline.
- **Success Criteria**: The script emits a `drift_report.json` containing the comparison.
- **Edge Cases**: Missing baseline, failed harness execution, non-deterministic drift noise.
