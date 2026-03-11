#### 1. Context & Goal
- **Objective**: Refactor the Regression Comparison Engine to read from separated `scorecard.json` files instead of monolithic run artifacts.
- **Trigger**: The recent `RunArtifactGeneration` and `ScorecardNormalizationRefactor` shifted the architecture to append-friendly split artifacts. However, the regression engine (`promptops/runs/compare.py`) still expects monolithic artifacts with a top-level `scorecard` key.
- **Impact**: Enables the regression engine to function correctly with the new `promptops-artifacts` branch topology, unblocking regression gates in GOVERNANCE.

#### 2. File Inventory
- **Create**: None
- **Modify**: `promptops/runs/compare.py` (Refactor to parse `scorecard.json` files directly instead of expecting a nested `"scorecard": {"normalized_metrics": {}}` structure).
- **Read-Only**: `README.md` (append-friendly immutable artifacts principle), `promptops/schemas/scorecard.schema.json` (expected input shape), `promptops/schemas/regression-policy.schema.json` (policy definitions).

#### 3. Implementation Spec
- **Harness Architecture**: The regression engine acts as an evaluation gate that compares two separated `scorecard.json` files based on a policy.
- **Run Request Format**: N/A
- **Run Artifact Format**: The input candidate and baseline are now strictly validated `scorecard.json` files.
- **Pseudo-Code**:
  - Parse CLI args: `<candidate_scorecard.json>` `<baseline_scorecard.json>` `<policy.yaml>` `<output_report.json>`
  - Load `candidate` and `baseline` JSON files.
  - Extract metrics by reading `candidate.get("normalized_metrics", {})` instead of traversing `candidate.get("scorecard", {}).get("normalized_metrics", {})`.
  - Execute policy rules iterating over metric floors and allowed deltas.
  - Output a `regression_report.json`.
- **Baseline and Regression Flow**: The baseline provided to the script will be a resolved `scorecard.json` artifact retrieved from the `promptops-artifacts` branch.
- **Dependencies**: CONTRACTS: `scorecard.schema.json`, `regression-policy.schema.json`, `regression-report.schema.json`.

#### 4. Test Plan
- **Verification**: Run `python promptops/runs/compare.py test-fixtures/mock-candidate-scorecard.json test-fixtures/mock-baseline-scorecard.json promptops/policies/regression.yaml test-fixtures/mock-report.json` and validate output against schema.
- **Success Criteria**: Script completes without KeyError and correctly parses the top-level metrics to emit a valid regression report.
- **Edge Cases**: Missing metric in candidate, empty policy file.
