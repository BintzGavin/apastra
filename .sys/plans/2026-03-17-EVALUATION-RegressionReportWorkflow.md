#### 1. Context & Goal
- **Objective**: Create a bash script to formalize the regression report generation and storage workflow.
- **Trigger**: The `README.md` conceptually defines a regression report as "Policy-evaluated candidate vs baseline comparison: pass/fail, warnings, evidence deltas." Currently, `compare.py` outputs a raw report, but there is no formalized, validated process connecting this script to the `derived-index/regressions/` directory structure.
- **Impact**: This unlocks the automated creation of immutable regression reports in the correct directory, which GOVERNANCE regression gates depend on to make promotion decisions.

#### 2. File Inventory
- **Create**: `promptops/runs/generate_regression_report.sh` (Bash script to orchestrate regression comparison and validate/store the report)
- **Modify**: `docs/status/EVALUATION.md` (Update version and log completion)
- **Read-Only**: `README.md` (Regression report definition), `promptops/schemas/regression-report.schema.json` (Schema for validation), `promptops/runs/compare.py` (CLI engine)

#### 3. Implementation Spec
- **Harness Architecture**: Acts as the final step in the evaluation pipeline, taking outputs from a candidate and a baseline to produce a validated report.
- **Run Request Format**: N/A for this script.
- **Run Artifact Format**: Relies on `scorecard.json` from the candidate and baseline artifacts.
- **Pseudo-Code**:
  - Accept parameters: candidate scorecard, baseline scorecard, policy file, report ID.
  - Execute `python promptops/runs/compare.py <candidate> <baseline> <policy> <temp_report.json>`.
  - Validate `temp_report.json` against `regression-report.schema.json` using `npx ajv-cli`.
  - Move the validated report to `derived-index/regressions/<report_id>.json`.
- **Baseline and Regression Flow**: Formalizes the regression comparison flow by producing the final immutable report.
- **Dependencies**: CONTRACTS schemas (`regression-report.schema.json`), RUNTIME resolver, GOVERNANCE policy files (`promptops/policies/regression.yaml`).

#### 4. Test Plan
- **Verification**: Execute `promptops/runs/generate_regression_report.sh` with valid dummy scorecards and policy to verify it generates a valid report.
- **Success Criteria**: A JSON file appears in `derived-index/regressions/` that passes schema validation.
- **Edge Cases**: Missing baseline file, invalid policy format, or `compare.py` outputting a schema-invalid report.
