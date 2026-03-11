#### 1. Context & Goal
- **Objective**: Implement a standalone metrics normalizer to produce the Scorecard for run artifacts.
- **Trigger**: The `README.md` requires a "Normalized metrics summary for a run, including metric definitions and metric versioning" for the Scorecard, which is currently stubbed in the BYO reference adapter.
- **Impact**: Unlocks the ability to define standardized regression policies based on normalized metrics and sets the foundation for baseline establishment and regression comparison.

#### 2. File Inventory
- **Create**: A normalizer script to compute a normalized scorecard from raw run metrics and update the run artifact.
- **Modify**: `promptops/harnesses/reference-adapter/run.py` (Update the reference harness to call the new scorecard normalizer during artifact generation)
- **Read-Only**: `README.md`, `promptops/schemas/scorecard.schema.json`, `promptops/schemas/run-artifact.schema.json`

#### 3. Implementation Spec
- **Harness Architecture**: The scorecard normalizer will accept an existing run artifact (e.g., from a BYO harness), calculate normalized metrics across cases, and inject the `scorecard` object back into the artifact.
- **Run Request Format**: No changes.
- **Run Artifact Format**: The `scorecard` object must include `normalized_metrics` (e.g., averaged accuracy, latency) and `metric_definitions` (type, range, versions) according to `promptops/schemas/scorecard.schema.json`.
- **Pseudo-Code**:
  ```python
  def normalize_metrics(run_artifact_path):
      # Load run artifact
      # Extract per-case evaluator outputs
      # Aggregate metrics (e.g., mean accuracy)
      # Define metric schemas and versions
      # Update run_artifact['scorecard']
      # Save run artifact
  ```
- **Baseline and Regression Flow**: Scorecards are the prerequisite for baselines.
- **Dependencies**: CONTRACTS `scorecard.schema.json` and `run-artifact.schema.json` are required.

#### 4. Test Plan
- **Verification**: Run the adapter and validate the generated artifact:
  ```bash
  mkdir -p mock-output
  echo '{"revision_ref": "mock"}' > mock-request.json
  python promptops/harnesses/reference-adapter/run.py mock-request.json mock-output
  npx ajv-cli validate -s promptops/schemas/run-artifact.schema.json -d mock-output/run_artifact.json --spec=draft2020 --strict=false
  ```
- **Success Criteria**:
  ```bash
  jq -e '.scorecard.normalized_metrics' mock-output/run_artifact.json > /dev/null
  jq -e '.scorecard.metric_definitions' mock-output/run_artifact.json > /dev/null
  ```
- **Edge Cases**:
  ```bash
  jq '.cases = []' mock-output/run_artifact.json > mock-output/run_artifact_empty.json
  jq -e '.scorecard.normalized_metrics' mock-output/run_artifact_empty.json > /dev/null
  ```
