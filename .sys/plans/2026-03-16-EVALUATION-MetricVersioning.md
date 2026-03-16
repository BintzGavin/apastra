#### 1. Context & Goal
- **Objective**: Implement metric versioning in scorecard normalizer.
- **Trigger**: The docs/vision.md and README.md define the "Scorecard" as needing to include metric definitions and metric versioning. The CONTRACTS schema for `scorecard` includes a `metric_definitions` field that can contain versioning info, but the normalizer currently doesn't implement or extract metric versions correctly if they exist on the `evaluator_outputs` items or properly inject a version in the generated `scorecard.json` metric definitions.
- **Impact**: Unlocks verifiable historical comparisons and prevents silent semantic drift in scorecards.

#### 2. File Inventory
- **Create**: None
- **Modify**: `promptops/runs/normalize.py` (Add metric versioning extraction and injection).
- **Read-Only**: `promptops/schemas/scorecard.schema.json`, `docs/vision.md`, `README.md`

#### 3. Implementation Spec
- **Harness Architecture**: The `promptops/runs/normalize.py` must be updated to look for `metric_version` on each evaluator output dictionary within `cases.jsonl` if it exists. And it must output the metric definition including the version.
- **Run Request Format**: No changes.
- **Run Artifact Format**: The `scorecard.json` will now include a `metric_definitions` object where each definition adheres to the schema and includes a `version`.
- **Baseline and Regression Flow**: Not applicable.
- **Pseudo-Code**:
  - For each `eval_output` item in `case.get("evaluator_outputs", [])`, look for a `metric_version` key. If present, extract it.
  - Exclude `metric_version` from the numeric scores to be averaged.
  - Map the metric keys back to their extracted versions.
  - When building the `metric_definitions` object for the final scorecard, inject the extracted `version` for each key, defaulting to `1.0.0` if not present.
- **Dependencies**: CONTRACTS (`scorecard.schema.json`).

#### 4. Test Plan
- **Verification**: cat promptops/runs/normalize.py | grep -A 10 metric_version
- **Success Criteria**: The `normalize.py` script correctly extracts the `metric_version` from evaluator outputs, ignores it when averaging scores, and assigns it in the final `metric_definitions`.
- **Edge Cases**: Missing `metric_version` key should default to `1.0.0`.