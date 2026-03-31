#### 1. Context & Goal
- **Objective**: Implement cost budget enforcement in harness adapters to hard-stop runs that exceed a dollar threshold.
- **Trigger**: The docs/vision.md file outlines a cost budget enforcement requirement in its Proposed Expansions section, stating that a cost_budget field on suites should hard-stop runs that exceed a dollar threshold.
- **Impact**: Unlocks safe automated evaluation of cost-intensive suites and prevents unexpected billing spikes.

#### 2. File Inventory
- **Create**: None
- **Modify**: promptops/harnesses/reference-adapter/run.py
- **Read-Only**: docs/vision.md, promptops/schemas/suite.schema.json, promptops/schemas/run-request.schema.json, promptops/runs/8dd64b79-a419-47e0-ba5f-219643c93cc7/run_manifest.json

#### 3. Implementation Spec
- **Harness Architecture**: The reference harness adapter must be modified to read `budgets.cost_budget` (or `budgets.cost`) from the run request. During the execution loop, it should accumulate token costs. If the accumulated total cost exceeds the budget threshold, the harness must halt execution immediately. It will write the partial results, mark the run's `status` as `budget_exceeded` in `run_manifest.json`, and write an explicit failure entry to a new `failures.json` artifact containing the failure reason.
- **Run Request Format**: Reads `budgets.cost` or `budgets.cost_budget`.
- **Run Artifact Format**: Updates `total_cost` and `status` in `run_manifest.json` and creates/writes to `failures.json` when the budget is exceeded.
- **Pseudo-Code**:
  cost_budget = req.get("budgets", {}).get("cost_budget", float("inf"))
  total_cost = 0.0
  failures = []
  for case in dataset:
    cost = execute_case_and_get_cost(case)
    total_cost += cost
    if total_cost > cost_budget:
      failures.append({"reason": "Cost budget exceeded"})
      status = "budget_exceeded"
      break
  write_run_manifest(total_cost, status)
  if failures:
    write_failures_json(failures)
- **Baseline and Regression Flow**: Not applicable for halting logic, but total_cost is recorded for downstream regression comparison.
- **Dependencies**: CONTRACTS schemas for suite and run_request already support budgets. RUNTIME resolver must pass budgets to the adapter.

#### 4. Test Plan
- **Verification**: Run `promptops/harnesses/reference-adapter/run.py` with a dummy run request containing a `cost_budget` of `0.001` and verify the output artifacts.
- **Success Criteria**: The harness writes a `run_manifest.json` with `status: budget_exceeded` and a `failures.json` containing the budget exceeded reason.
- **Edge Cases**: No budget specified, zero budget, budget exceeded on the exact first token.
