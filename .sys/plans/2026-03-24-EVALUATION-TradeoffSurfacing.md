#### 1. Context & Goal
- **Objective**: Implement tradeoff surfacing in the regression report.
- **Trigger**: The vision document explicitly requires showing quality vs cost vs latency changes in the regression report, but `compare.py` currently only surfaces metrics that have explicitly defined rules in the policy file.
- **Impact**: Unlocks the ability for teams to see how prompt changes affect cost and latency, even when they aren't explicitly gated, leading to more informed review decisions.

#### 2. File Inventory
- **Create**: None
- **Modify**: `promptops/runs/compare.py` (Update `compare.py` to loop over all metrics in `candidate_metrics` and `baseline_metrics`, surfacing metrics not covered by explicit policy rules as informational evidence).
- **Read-Only**: `docs/vision.md`, `promptops/schemas/regression-report.schema.json`

#### 3. Implementation Spec
- **Harness Architecture**: N/A
- **Run Request Format**: N/A
- **Run Artifact Format**: N/A
- **Baseline and Regression Flow**:
  - The Regression Comparison Engine (`compare.py`) loops through the keys in both the `candidate_metrics` and `baseline_metrics` (obtained from their respective scorecards).
  - Any metric that does *not* have an explicit rule in the provided `policy` is added to the `evidence` array with a status of `"info"`, and its calculated delta.
  - Metrics with explicit rules are still processed and evaluated for "pass", "fail", or "warning" status.
- **Pseudo-Code**:
  - First, gather all unique metric names from candidate and baseline scorecards.
  - Create a set of `ruled_metrics` based on the policy rules.
  - Iterate through the policy rules, processing and appending rule-based evidence.
  - Iterate through the remaining `ungated_metrics`. For each, calculate the delta between candidate and baseline, and append to the evidence array with a status of `"info"`.
- **Dependencies**: Depends on the existing GOVERNANCE regression-policy schema and the CONTRACTS regression-report schema (which allows arbitrary evidence objects).

#### 4. Test Plan
- **Verification**: `python promptops/runs/compare.py`
- **Success Criteria**: `compare.py` accepts candidate, baseline, and policy inputs, producing a regression report that surfaces un-gated metrics (e.g. cost, latency) with an "info" status.
- **Edge Cases**: Missing metrics in either candidate or baseline; un-gated metrics with identical values.