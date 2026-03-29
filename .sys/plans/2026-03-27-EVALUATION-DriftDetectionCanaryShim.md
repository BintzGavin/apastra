#### 1. Context & Goal
- **Objective**: Implement drift detection for production prompt monitoring by generating canary suite execution script.
- **Trigger**: The docs/vision.md describes an expansion feature for 'drift detection' via canary suites that run on a schedule to catch post-ship quality erosion.
- **Impact**: Enables GOVERNANCE to monitor production prompts and trigger alerts when model providers silently update and cause output drift.

#### 2. File Inventory
- **Create**: `promptops/runs/canary-shim.sh` (Executes canary suites and compares against production baseline)
- **Modify**: None
- **Read-Only**: `docs/vision.md`, `README.md`

#### 3. Implementation Spec
- **Harness Architecture**: The `canary-shim.sh` script will wrap the existing harness runner (`runner-shim.sh`) but specifically target a canary suite.
- **Run Request Format**: The script will accept a canary configuration file (YAML) defining the suite_ref, schedule, and alert configuration.
- **Run Artifact Format**: The script will produce standard run artifacts via the runner, then execute `compare.py` against the known production baseline.
- **Pseudo-Code**:
  1. Parse canary YAML to get `suite_ref`.
  2. Generate a run request for the `suite_ref`.
  3. Invoke `runner-shim.sh` with the request.
  4. Invoke `compare.py` using the new scorecard and the production baseline.
  5. Check if the regression report status is 'fail' or 'warning'.
  6. Emit drift alert (print to stdout) if drift is detected.
- **Baseline and Regression Flow**: Uses existing baseline and regression comparison logic to detect drift.
- **Dependencies**: Requires RUNTIME resolver (to resolve `suite_ref`), CONTRACTS schemas (run-request, regression-report).

#### 4. Test Plan
- **Verification**: `bash promptops/runs/canary-shim.sh test-canary.yaml`
- **Success Criteria**: The script correctly invokes the harness and comparison engine, and prints an alert if drift is detected.
- **Edge Cases**: Missing baseline, failed run request generation, invalid canary configuration.
