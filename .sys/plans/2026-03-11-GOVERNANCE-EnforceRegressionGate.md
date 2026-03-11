#### 1. Context & Goal
- **Objective**: Enforce the regression gate by removing the graceful bypass for missing reports.
- **Trigger**: The regression comparison engine (`compare.py`) has been implemented by the EVALUATION domain, making the temporary bypass in the CI gate a severe anti-pattern that violates the "Regression outcomes must gate merges" primitive.
- **Impact**: Enforces that merges are strictly blocked unless a passing regression report is provided, fulfilling the required status check audit trail.

#### 2. File Inventory
- **Create**: None
- **Modify**: `.github/workflows/regression-gate.yml` (remove bypass and enforce hard failure on missing report)
- **Read-Only**: `README.md` (Required status checks section), `docs/status/EVALUATION.md` (verified engine implementation)

#### 3. Implementation Spec
- **Policy Architecture**: The workflow must read `reports/regression_report.json`. If missing, it must fail the check run rather than skipping it, as the engine dependency is now fulfilled.
- **Workflow Design**: Update `Check Regression Report Status` step logic to fail (return status 1) instead of succeeding when the report file does not exist.
- **CODEOWNERS Patterns**: N/A
- **Promotion Record Format**: N/A
- **Delivery Target Format**: N/A
- **Dependencies**: EVALUATION's regression report format is stable; CONTRACTS schemas are stable.

#### 4. Test Plan
- **Verification**: Run the gate workflow without a regression report present and verify it fails.
- **Success Criteria**: The GitHub Action step fails and blocks the merge when the report is missing.
- **Edge Cases**: Empty files or malformed JSON should also be handled by the JSON query tool failing, which correctly results in a blocked gate.
