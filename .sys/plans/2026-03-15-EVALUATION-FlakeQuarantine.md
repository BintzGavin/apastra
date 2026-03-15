#### 1. Context & Goal
- **Objective**: Implement flake quarantine and tracking to prevent flakiness from silently passing as random noise and to support variance-aware regression gating.
- **Trigger**: The docs/vision.md requirement "Quarantine flaky cases and track their flake rate; do not let flakiness silently pass as 'random noise'." is currently missing from the scorecard normalization and regression comparison logic.
- **Impact**: Unlocks reliable regression comparisons by isolating flaky evaluation cases from stable metrics, directly impacting GOVERNANCE release gates which depend on accurate, noise-free regression reports.

#### 2. File Inventory
- **Create**: None.
- **Modify**: `promptops/schemas/scorecard.schema.json` (add `flake_rates` to track per-metric flakiness), `promptops/runs/normalize.py` (calculate flake rates across trials and include in the scorecard), `promptops/runs/compare.py` (read flake rates and apply variance-aware quarantine logic or warnings).
- **Read-Only**: `docs/vision.md`, `promptops/schemas/run-artifact.schema.json`, `promptops/schemas/regression-policy.schema.json`.

#### 3. Implementation Spec
- **Harness Architecture**: The `scorecard.schema.json` will be extended to include a `flake_rates` map, storing the proportion of trials that resulted in a score divergence (e.g. passing vs failing) for each case/metric.
- **Run Request Format**: Unchanged.
- **Run Artifact Format**: The generated `scorecard.json` will now output a `flake_rates` object alongside `variance`.
- **Pseudo-Code**:
  - In `normalize.py`: For each metric, analyze the distribution of scores across trials. If a metric yields both 1.0 (pass) and 0.0 (fail) or significantly varying continuous scores for the same `case_id`, compute its flake rate and append to `flake_rates`.
  - In `compare.py`: When processing `candidate_metrics`, check the corresponding `flake_rates`. If a metric is deemed flaky (above a set threshold), it should be optionally quarantined (ignored from blocker status) and explicitly flagged with a "flaky" or "warning" status in the regression evidence, so it doesn't mask true regressions.
- **Baseline and Regression Flow**: Flaky metrics in candidates vs baselines are surfaced to GOVERNANCE without failing the entire suite incorrectly, ensuring variance-aware gating.
- **Dependencies**: CONTRACTS (schema updates for scorecard), RUNTIME resolver availability, GOVERNANCE policy files needed.

#### 4. Test Plan
- **Verification**: `echo "No tests to run for Architect Planner"`
- **Success Criteria**: The executor updates `scorecard.schema.json`, `normalize.py`, and `compare.py` to identify and report flaky metrics.
- **Edge Cases**: Metric with high variance but consistent average; metric failing in all trials vs failing in only a subset (true flake).