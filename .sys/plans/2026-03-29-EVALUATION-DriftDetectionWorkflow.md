#### 1. Context & Goal
- **Objective**: Implement the Drift Detection workflow to execute canary suites against production baselines and emit drift reports.
- **Trigger**: The docs/vision.md "Drift detection" expansion calls for canary suites that run on a schedule and compare results against production baselines to emit drift reports.
- **Impact**: Unlocks post-ship quality monitoring, allowing teams to detect when model providers silently update and cause output drift.

#### 2. File Inventory
- **Create**:
  - `promptops/runs/run_canary.sh`: Bash script that takes a canary suite request, executes the harness, and compares the result to the established production baseline to generate a drift report.
- **Modify**:
  - None
- **Read-Only**:
  - `docs/vision.md`
  - CONTRACTS schemas

#### 3. Implementation Spec
- **Harness Architecture**: The `run_canary.sh` script will act as an orchestration layer. It will invoke the existing `runner-shim.sh` to execute the canary suite and then invoke `compare.py` to compare the resulting scorecard against the provided production baseline.
- **Run Request Format**: Uses the existing run request format, but specifically configured for canary test cases.
- **Run Artifact Format**: Standard run artifact format (`run_manifest.json`, `scorecard.json`, etc.), with the addition of a Drift Report (which follows the regression report schema).
- **Pseudo-Code**:
    # run_canary.sh <adapter_yaml> <run_request> <baseline_scorecard> <policy_file> <output_dir>
    # 1. Invoke runner-shim.sh to execute the canary suite
    # 2. Extract the new scorecard.json
    # 3. Invoke compare.py with the new scorecard and the baseline_scorecard
    # 4. Save the output as drift_report.json
- **Baseline and Regression Flow**: Drift reports are structurally identical to regression reports, comparing a new run (canary) against an immutable baseline.
- **Dependencies**: CONTRACTS regression report schema and suite schema must be available. RUNTIME resolver must be available to resolve prompts during harness execution.

#### 4. Test Plan
- **Verification**: Run `bash promptops/runs/run_canary.sh promptops/harnesses/reference-adapter/adapter.yaml test_req.json test_baseline.json test_policy.yaml output/` with mock files to verify it generates a `drift_report.json`.
- **Success Criteria**: The `run_canary.sh` script successfully invokes the harness and comparison engine, writing a valid `drift_report.json` that conforms to the regression report schema.
- **Edge Cases**: Missing baseline file, harness execution failure, or missing policy file should fail gracefully with a clear error message.
