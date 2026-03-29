#### 1. Context & Goal
- **Objective**: Implement drift detection for production prompt monitoring via canary suite execution.
- **Trigger**: The docs/vision.md expansion explicitly proposes drift detection capabilities that execute a canary suite on a schedule and emit a drift report comparing canary results against the production baseline when model drift occurs.
- **Impact**: Unlocks continuous post-ship evaluation of production prompts, giving teams confidence that "silent" model provider updates haven't eroded the quality or behavior of previously shipped prompts. This complements pre-ship regression gating.

#### 2. File Inventory
- **Create**:
  - `promptops/runs/generate_drift_report.sh`: Generates a drift report comparing a canary scorecard against the established baseline.
- **Modify**: []
- **Read-Only**:
  - `docs/vision.md` (Expansion 2: Drift detection — production prompt monitoring)
  - `promptops/schemas/drift-report.schema.json` (Drift report format requirement)
  - `promptops/schemas/canary-suite.schema.json` (Canary suite structure, read-only)

#### 3. Implementation Spec
- **Harness Architecture**: The `generate_drift_report.sh` script will take a `candidate_scorecard.json` (from the canary suite run), a `baseline_scorecard.json` (the production baseline), and a `policy_file.yaml` (the regression/drift policy).
- **Run Request Format**: Uses standard run request schema for the underlying canary suite run (relies on `run_request.schema.json`).
- **Run Artifact Format**: Will produce a `drift_report.json` structurally identical to the schema specification (using `compare.py` under the hood, but validating against the `drift-report.schema.json`).
- **Pseudo-Code**:
  ```bash
  # generate_drift_report.sh
  1. Validate input arguments (candidate, baseline, policy, report_id).
  2. Call compare.py to generate temporary drift data.
  3. Format output of compare.py to match drift-report.schema.json mapping status to drift_detected (true if status is "fail" or "warning", false otherwise).
  4. Validate temporary data against drift-report.schema.json using ajv-cli.
  5. Write validated report to derived-index/regressions/<report_id>.json (or standard output).
  ```
- **Baseline and Regression Flow**: Drift comparison mirrors regression comparison but uses a specific, scheduled "canary suite" and alerts based on the resulting drift report.
- **Dependencies**:
  - `promptops/schemas/drift-report.schema.json`
  - `promptops/runs/compare.py`

#### 4. Test Plan
- **Verification**: Run `generate_drift_report.sh` with a dummy candidate, baseline, and policy.
- **Success Criteria**: The script exits 0 and produces a valid drift report JSON file matching the schema.
- **Edge Cases**: Empty input scorecards, missing files, validation failures.
