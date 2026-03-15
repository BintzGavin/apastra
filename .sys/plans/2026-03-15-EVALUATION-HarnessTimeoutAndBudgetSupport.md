#### 1. Context & Goal
- **Objective**: Implement budget and timeout enforcement in the BYO harness adapter.
- **Trigger**: The vision document specifies that the benchmark suite declares `budgets` and `timeouts` which control cost and determinism tradeoffs, but the reference adapter currently does not enforce them.
- **Impact**: Unlocks deterministic control over evaluation runs, preventing runaway execution time and excessive token costs, which is crucial for regression gating.

#### 2. File Inventory
- **Modify**: `promptops/harnesses/reference-adapter/run.py` (Add logic to parse and enforce `budgets` and `timeouts` during suite execution)
- **Modify**: `promptops/harnesses/reference-adapter/adapter.yaml` (Add `timeouts` and `budgets` to the `capabilities` list)
- **Read-Only**: `docs/vision.md`, `promptops/schemas/run-request.schema.json`, `promptops/schemas/suite.schema.json`

#### 3. Implementation Spec
- **Harness Architecture**:
  - Update `promptops/harnesses/reference-adapter/adapter.yaml` to declare `budgets` and `timeouts` in its capabilities.
  - Modify `promptops/harnesses/reference-adapter/run.py` to extract `budgets` and `timeouts` from the `run_request.json` payload.
  - Implement a mechanism (e.g., using `concurrent.futures.TimeoutError` or similar standard library constructs) to enforce the `time` budget and any generic `timeouts` provided.
  - Track accumulated token cost during execution and short-circuit/fail the run or case if the `cost` budget is exceeded.
- **Run Request Format**: Reads `budgets` (e.g., `{"cost": 1.0, "time": 300}`) and `timeouts` (e.g., `{"case_timeout": 30}`) fields.
- **Run Artifact Format**: Any aborted run due to timeout or budget overrun should be reflected in the `status` field of `run_manifest.json` as `"failure"` or a specific `"timeout"`/`"budget_exceeded"` state, with details appended to `failures.json`.
- **Pseudo-Code**:
  - `start_time = time.time()`
  - `cost_accumulated = 0.0`
  - `budget_cost = request.get('budgets', {}).get('cost', float('inf'))`
  - `timeout = request.get('timeouts', {}).get('case_timeout', None)`
  - `For each case:`
    - `If cost_accumulated >= budget_cost: fail_run('Budget exceeded')`
    - `Try:`
      - `execute_case(case) with timeout`
      - `cost_accumulated += get_case_cost()`
    - `Except TimeoutError: fail_case('Timeout exceeded')`
- **Baseline and Regression Flow**: No direct impact, as regressions operate on successful run artifacts. Failed runs naturally block promotion.
- **Dependencies**: Depends on the existing CONTRACTS schemas for `run-request` and `suite`; RUNTIME resolver is already integrated in `run.py`.

#### 4. Test Plan
- **Verification**: cat .sys/plans/2026-03-15-EVALUATION-HarnessTimeoutAndBudgetSupport.md
- **Success Criteria**: The harness successfully aborts and outputs a failure artifact when given a mock run request with a budget lower than the cost, or a timeout shorter than execution time.
- **Edge Cases**: Zero budgets, missing budgets, negative timeouts.