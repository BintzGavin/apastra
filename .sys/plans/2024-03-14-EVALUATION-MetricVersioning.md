#### 1. Context & Goal
- **Objective**: Implement metric versioning in the scorecard normalizer.
- **Trigger**: `docs/vision.md` requires that run artifacts record "Normalized metrics summary for a run, including metric definitions and metric versioning." to "prevent silent semantic drift in scorecards", but `normalize.py` currently only outputs `metric_definitions` without any metric versioning information.
- **Impact**: Enables long-term comparability of metrics by tracking evaluator evolution and metric versions, as required by the vision.

#### 2. File Inventory
- **Create**: None
- **Modify**: `promptops/runs/normalize.py`
- **Read-Only**: `promptops/schemas/scorecard.schema.json`, `docs/vision.md`

#### 3. Implementation Spec
- **Harness Architecture**: N/A
- **Run Request Format**: N/A
- **Run Artifact Format**: The `metric_definitions` object in `scorecard.json` must be updated to include metric versioning information.
- **Pseudo-Code**:
  - Update `normalize.py` to extract `metric_version` from `evaluator_outputs` in `cases.jsonl` if present.
  - In `normalize_scorecard`, when building `metric_definitions`, include `version: <extracted_version>` (defaulting to "1.0.0" if not present).
- **Baseline and Regression Flow**: Regressions will be able to compare metric versions to ensure comparability.
- **Dependencies**: CONTRACTS: `scorecard.schema.json`

#### 4. Test Plan
- **Verification**: `echo '{"evaluator_outputs": [{"test_metric": 1.0, "metric_version": "2.0.0"}]}' > test_cases.jsonl && python3 promptops/runs/normalize.py test_cases.jsonl test_scorecard.json && grep "version" test_scorecard.json && rm test_cases.jsonl test_scorecard.json`
- **Success Criteria**: The output `scorecard.json` contains `version` fields within the `metric_definitions` object.
- **Edge Cases**: Evaluator outputs without explicit versioning should default to "1.0.0".
