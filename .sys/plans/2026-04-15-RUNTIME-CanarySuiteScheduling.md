#### 1. Context & Goal
- **Objective**: Implement drift detection via scheduled canary suites.
- **Trigger**: The docs/vision.md file specifies "Expansion 2: Drift detection — production prompt monitoring" to catch post-ship quality erosion caused by silent model updates.
- **Impact**: Enables teams to monitor production prompts for drift over time by running a small set of critical assertions on a schedule and comparing results to the production baseline.

#### 2. File Inventory
- **Create**:
  - promptops/runtime/canary.py (New file for defining and running canary schedules).
  - promptops/canaries/test-canary.yaml (Mock canary spec file for testing).
- **Modify**:
  - promptops/runtime/cli.py (Add a canary command to trigger the canary runner).
- **Read-Only**:
  - docs/vision.md (Expansion 2: Drift detection).
  - promptops/schemas/suite.schema.json

#### 3. Implementation Spec
- **Resolver Architecture**: The canary runner will be an entrypoint that loads a canary definition file, resolves the target suite, executes it via the configured harness adapter, and compares the resulting scorecard against a baseline.
- **Manifest Format**: Unchanged. Canary definitions will be stored separately (e.g., promptops/canaries/).
- **Pseudo-Code**:
  ```python
  def run_canary(canary_path):
      # Load the canary YAML definition.
      # Extract the suite_ref and schedule.
      # Trigger a run request for the suite_ref.
      # Execute the run request using the RunnerShim.
      # Compare the generated scorecard with the designated baseline (e.g., prod current).
      # If regressions are detected and alert.on_regression is true, emit an alert via the configured channel.
  ```
- **Harness Contract Interface**: No changes to the core harness contract, as the canary runner orchestrates existing RunnerShim and regression capabilities.
- **Dependencies**: Requires the creation of a canary schema in the CONTRACTS domain to validate canary definitions before the runtime can fully integrate it.

#### 4. Test Plan
- **Verification**: Run `python -m promptops.runtime.cli canary promptops/canaries/test-canary.yaml` to verify the runner logic using the mock file created.
- **Success Criteria**: The CLI should parse the canary definition, invoke the suite, and successfully generate a drift report comparing the run output to the baseline.
- **Edge Cases**: Missing suite reference, invalid canary schema, baseline not found, harness execution failure.
