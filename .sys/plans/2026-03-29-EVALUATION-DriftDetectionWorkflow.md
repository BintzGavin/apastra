#### 1. Context & Goal
- **Objective**: Implement drift detection by analyzing canary suite runs.
- **Trigger**: "docs/vision.md" specifies "Drift detection: canary suites that run on a schedule... and emit drift reports when model provider updates cause output changes".
- **Impact**: Unlocks production prompt monitoring and post-ship quality erosion detection, fulfilling a P1 expansion priority.

#### 2. File Inventory
- **Create**: `promptops/runs/generate_drift_report.sh`, `promptops/runs/detect_drift.py`
- **Modify**: None
- **Read-Only**: `promptops/schemas/canary-suite.schema.json`, `promptops/schemas/drift-report.schema.json`, `docs/vision.md`, `README.md`

#### 3. Implementation Spec
- **Harness Architecture**: Reuses the minimal adapter interface but operates in a scheduled "canary" mode. The system evaluates current model outputs against an established production baseline.
- **Run Request Format**: Leverages existing run request metadata (`prompt_digest`, `dataset_digest`, `model_matrix`, `evaluator_refs`).
- **Run Artifact Format**: A `drift_report.json` schema containing `baseline_ref`, `current_ref`, a boolean `drift_detected` flag, and an `evidence` array detailing metrics that exceeded thresholds.
- **Pseudo-Code**:
  - Read `canary_scorecard` and `baseline_scorecard`.
  - For each metric in the scorecard, compute `delta`.
  - If `delta` exceeds an implicitly or explicitly defined drift threshold (e.g., from `canary-suite.schema.json`), flag `drift_detected = True` and append to `evidence`.
  - Write `drift_report.json` and validate against `drift-report.schema.json`.
- **Baseline and Regression Flow**: Uses the same `derived-index/baselines/` for reference but applies a specific drift sensitivity check instead of merge-blocking regression rules.
- **Dependencies**: Depends on `promptops/schemas/drift-report.schema.json` (CONTRACTS) and the ability to schedule/execute runs.

#### 4. Test Plan
- **Verification**: Execute `generate_drift_report.sh dummy-canary.json dummy-baseline.json dummy-drift-report.json` using mock scorecards.
- **Success Criteria**: A valid `drift_report.json` is generated that passes `ajv-cli` schema validation against `drift-report.schema.json`.
- **Edge Cases**: Missing metrics in current vs baseline, identical values (no drift), values exactly at the threshold, and outputs varying non-deterministically without crossing the drift threshold.
