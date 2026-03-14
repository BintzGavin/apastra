#### 1. Context & Goal
- **Objective**: Implement support for multiple trials and calculate score variance in the scorecard normalizer.
- **Trigger**: `docs/vision.md` requires that run artifacts record variance when multiple trials are configured ("Support trials and record variance; regression policies should be variance-aware"), but `normalize.py` only computes an average.
- **Impact**: Unlocks variance-aware regression gating and helps identify flaky evaluation cases.

#### 2. File Inventory
- **Create**: None
- **Modify**: `promptops/runs/normalize.py` (Add statistical variance calculation for metric scores), `promptops/harnesses/reference-adapter/run.py` (Execute multiple trials if `trials` > 1 is specified).
- **Read-Only**: `promptops/schemas/scorecard.schema.json`, `promptops/schemas/run-request.schema.json`, `docs/vision.md`.

#### 3. Implementation Spec
- **Harness Architecture**: N/A
- **Run Request Format**: Reads the `trials` integer field from the run request.
- **Run Artifact Format**: `scorecard.json` will include a `variance` object mapping metric names to their calculated variance.
- **Pseudo-Code**:
  - In `run.py`, read the `trials` key from `run_request.json` (default to 1).
  - Loop `trials` times when evaluating each case, appending each output to `per_trial_outputs` and evaluating each to append to `evaluator_outputs`.
  - In `normalize.py`, collect all scores for each metric. Calculate the mean (as currently done).
  - Calculate the variance using the population variance formula `sum((x - mean) ** 2) / count` for each metric.
  - Populate the `variance` field in the final scorecard object.
- **Baseline and Regression Flow**: Regressions can later use variance to dynamically adjust thresholds.
- **Dependencies**: CONTRACTS schemas required (`scorecard.schema.json`); RUNTIME resolver availability; GOVERNANCE policy files needed.

#### 4. Test Plan
- **Verification**: `python3 promptops/harnesses/reference-adapter/run.py dummy_request.json out_dir`
- **Success Criteria**: `scorecard.json` contains a `variance` object with numeric variance values for the evaluated metrics.
- **Edge Cases**: Zero variance for deterministic assertions; single trial resulting in 0 variance; missing trials key defaults to 1.
