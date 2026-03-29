#### 1. Context & Goal
- **Objective**: Implement `total_cost` tracking in run manifests and `cost_delta` in regression reports.
- **Trigger**: docs/vision.md refinement "First-class cost tracking" explicitly requires "Every run manifest should include total cost... Regression reports should include cost delta".
- **Impact**: Enables organizations to track the cost of evaluation runs natively and construct governance gates that monitor cost increases between baseline and candidate prompt specs.

#### 2. File Inventory
- **Create**: None
- **Modify**:
  - `promptops/harnesses/reference-adapter/run.py` (Add accumulated cost tracking and append `total_cost` to `run_manifest.json`)
  - `promptops/runs/compare.py` (Calculate `cost_delta` and append it to `regression_report.json`)
- **Read-Only**: `docs/vision.md`, `promptops/schemas/run-manifest.schema.json`, `promptops/schemas/regression-report.schema.json`

#### 3. Implementation Spec
- **Harness Architecture**:
  - In `run.py`, initialize an accumulator `total_cost = 0.0`. During case execution (simulated or real), retrieve token cost metrics if available, or accumulate a simulated cost.
  - Write `total_cost` to the output `run_manifest.json`.
  - Enforce `cost_budget` if declared in the `run_request.json` `budgets` field, stopping the run if `total_cost` exceeds it.
- **Run Request Format**: Unchanged, reads `budgets` field natively.
- **Run Artifact Format**: The `run_manifest.json` will now include a `total_cost` numeric field.
- **Pseudo-Code**:
  # In run.py:
  total_cost = 0.0
  cost_budget = req.get("budgets", {}).get("cost", float('inf'))
  # simulate case loop cost addition
  total_cost += 0.05
  if total_cost > cost_budget:
      manifest["status"] = "budget_exceeded"
      # break
  manifest["total_cost"] = total_cost

  # In compare.py:
  c_cost = candidate.get("manifest", {}).get("total_cost", 0)
  b_cost = baseline.get("manifest", {}).get("total_cost", 0)
  report["cost_delta"] = c_cost - b_cost
- **Baseline and Regression Flow**: `compare.py` reads `total_cost` from both candidate and baseline `run_manifest.json` (or extracted metadata) and emits `cost_delta` to the `regression_report.json`.
- **Dependencies**: Depends on recent CONTRACTS updates to `run-manifest.schema.json` and `regression-report.schema.json` to allow these fields.

#### 4. Test Plan
- **Verification**: Execute `./promptops/harnesses/reference-adapter/run.py` with a mock run request and verify `total_cost` is present in the output `run_manifest.json`. Execute `compare.py` with two mock artifacts and verify `cost_delta` is present in the output `regression_report.json`.
- **Success Criteria**: Validation of the generated `run_manifest.json` and `regression_report.json` passes using `ajv-cli` against their respective schemas.
- **Edge Cases**: Missing `total_cost` in legacy baseline artifacts, zero cost budgets.
