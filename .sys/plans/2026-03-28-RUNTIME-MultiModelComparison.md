#### 1. Context & Goal
- **Objective**: Implement multi-model comparison runtime support.
- **Trigger**: "Multi-model comparison" vision requirement from docs/vision.md.
- **Impact**: Enables EVALUATION harnesses to run suites across multiple models simultaneously and generate comparison scorecards with cost/quality/latency tradeoffs, unlocking "promotion candidate" workflows.

#### 2. File Inventory
- **Create**: promptops/runtime/compare.py (Comparison utilities)
- **Modify**: promptops/runtime/runner.py (Update runner to orchestrate the multi-model matrix execution and assemble the comparison scorecard)
- **Read-Only**: docs/vision.md, promptops/schemas/run-request.schema.json, promptops/schemas/suite.schema.json

#### 3. Implementation Spec
- **Resolver Architecture**: The resolver chain resolves the suite, taking note of the `model_matrix`. The runtime execution logic orchestrates runs for each model.
- **Manifest Format**: Manifest schemas support model_matrix already.
- **Pseudo-Code**:
  1. The runner parses the run request and extracts the `model_matrix`.
  2. For each model in the matrix, the runner executes the suite (or instructs the harness to do so).
  3. The results are aggregated into a comparison scorecard mapping model IDs to their respective metrics and costs.
- **Harness Contract Interface**: Harness input remains `run_request.json` with `model_matrix`. The `scorecard.json` schema supports metric mapping per model.
- **Dependencies**: EVALUATION domain must define the comparison scorecard schema if not already explicitly modeled. CONTRACTS schemas for `suite` and `run-request` already support `model_matrix`.

#### 4. Test Plan
- **Verification**: Run `python promptops/runtime/runner.py <run_request_with_multiple_models> <adapter> <out_dir>` and inspect `scorecard.json` to ensure results for all models are aggregated.
- **Success Criteria**: The scorecard contains aggregated metrics correctly mapped by model ID.
- **Edge Cases**: Empty model matrix (fallback to default), single model, harness adapter failing for one model but passing for others.
