#### 1. Context & Goal
- **Objective**: Spec the Regression Comparison Engine to compare candidate scorecards against baselines.
- **Trigger**: The README.md outlines a "Policy-driven regression detection model" that produces a regression report, but there is currently no engine to compare `promptops/runs/` scorecards against `derived-index/baselines/` and apply `promptops/policies/regression.yaml`.
- **Impact**: This unlocks the GOVERNANCE domain's ability to gate merges and promotions using required status checks based on the `regression_report.json` outputs.

#### 2. File Inventory
- **Create**:
  - `promptops/runs/compare.py`: CLI script that takes a candidate run artifact, a baseline run artifact, and a policy spec, then outputs a regression report.
- **Modify**: None.
- **Read-Only**:
  - `promptops/schemas/scorecard.schema.json`
  - `promptops/schemas/regression-policy.schema.json`
  - `promptops/schemas/regression-report.schema.json`
  - `promptops/schemas/baseline.schema.json`

#### 3. Implementation Spec
- **Baseline and Regression Flow**: The engine reads the baseline digest from `derived-index/baselines/<suite_id>.json`, fetches the corresponding baseline `scorecard.json` from the artifact store (or `promptops/runs/`), and fetches the candidate `scorecard.json`.
- **Regression Logic**:
  - Iterate through metrics defined in `promptops/policies/regression.yaml`.
  - Compare candidate values against baseline values.
  - Apply rules: absolute floors, allowed deltas, directionality.
  - Evaluate whether failures are "blockers" (fail checks) or "warnings" (require signoff).
- **Run Artifact Format**: The engine output is a `regression_report.json` matching the CONTRACTS schema, detailing pass/fail status, warnings, and evidence deltas.
- **Pseudo-Code**:
  ```python
  # Pseudo-code only
  def compare(candidate_path, baseline_path, policy_path, output_path):
      candidate_scorecard = load_json(candidate_path)["scorecard"]
      baseline_scorecard = load_json(baseline_path)["scorecard"]
      policy = load_yaml(policy_path)

      report = {"status": "pass", "blockers": [], "warnings": [], "deltas": {}}
      for metric, rules in policy.items():
          c_val = candidate_scorecard["normalized_metrics"].get(metric)
          b_val = baseline_scorecard["normalized_metrics"].get(metric)
          # Apply logic...

      write_json(report, output_path)
  ```
- **Dependencies**:
  - CONTRACTS schemas: `scorecard.schema.json`, `regression-policy.schema.json`, `regression-report.schema.json` (Available).
  - RUNTIME resolver: Not directly required for comparison, but needed for prior run step.
  - GOVERNANCE policy files: Required (`promptops/policies/regression.yaml`).

#### 4. Test Plan
- **Verification**: `python promptops/runs/compare.py test-fixtures/candidate.json test-fixtures/baseline.json test-fixtures/policy.yaml test-fixtures/regression_report.json`
- **Success Criteria**: `[ -f test-fixtures/regression_report.json ] && npx ajv-cli validate -s promptops/schemas/regression-report.schema.json -d test-fixtures/regression_report.json --spec=draft2020 --strict=false`
- **Edge Cases**:
  - Baseline missing: `rm -f test-fixtures/baseline.json && ! python promptops/runs/compare.py test-fixtures/candidate.json test-fixtures/baseline.json test-fixtures/policy.yaml test-fixtures/regression_report.json`
  - Metric missing in candidate: Ensure the engine flags it as a blocker or handles it gracefully according to policy.
