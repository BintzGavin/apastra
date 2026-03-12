#### 1. Context & Goal
- **Objective**: Enhance the regression gate workflow to provide rich PR annotations and a detailed Markdown summary of regression evidence.
- **Trigger**: The README.md promises "Checks API for rich PR annotations" and "Regression outcomes must gate merges" with visible evidence, but the current check only exits 1/0 without exposing metric deltas.
- **Impact**: Enforces transparency by automatically surfacing regression evidence (failing metrics, deltas, baselines) directly in the PR UI via GitHub Actions step summaries and annotations, making human review checkpoints explicit and auditable.

#### 2. File Inventory
- **Create**: None
- **Modify**: `.github/workflows/regression-gate.yml`
- **Read-Only**: `README.md`, `promptops/schemas/regression-report.schema.json`

#### 3. Implementation Spec
- **Policy Architecture**: The gate logic remains the same (blocking merges on fail/warning), but it now iterates over the `evidence` array from the regression report. It generates a Markdown table of all metrics, their candidate values, baseline values, and deltas, appending this to `$GITHUB_STEP_SUMMARY`.
- **Workflow Design**:
  - In `regression-gate.yml`, modify the `Check Regression Report Status` step.
  - Read `STATUS` from the report.
  - Use `jq` to format the `evidence` array into a Markdown table: `| Metric | Status | Candidate | Baseline | Delta | Message |` and append to `$GITHUB_STEP_SUMMARY`.
  - Loop through `evidence` items where `status == "fail"` and use `echo "::error title=Regression Failed::Metric \($metric): \($message)"`.
  - Exit 1 if overall status is not `pass`.
- **CODEOWNERS Patterns**: N/A
- **Promotion Record Format**: N/A
- **Delivery Target Format**: N/A
- **Dependencies**: EVALUATION regression report format (`reports/regression_report.json`) must reliably contain the `evidence` array.

#### 4. Test Plan
- **Verification**: Simulate the `jq` parsing logic on a dummy `regression_report.json` to ensure the Markdown table and `::error::` annotations are formatted correctly.
- **Success Criteria**: The `jq` script successfully transforms the JSON evidence into a valid Markdown table and emits proper GitHub Actions annotation commands without syntax errors.
- **Edge Cases**: Missing `evidence` array, missing `delta` values, and missing report file.