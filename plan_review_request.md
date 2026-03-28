1. Context & Goal
- Objective: Create an execution plan specification to implement multi-model comparison scorecard generation.
- Trigger: The docs/vision.md expansion feature "Multi-model comparison: run a suite against N models simultaneously and produce a comparison scorecard with per-model breakdowns and cost/quality/latency tradeoff surfaces" is not yet implemented.
- Impact: This enables the generation of comparative evaluation scorecards across different models, facilitating better model selection and tradeoff analysis.

2. File Inventory
- Create: /.sys/plans/YYYY-MM-DD-EVALUATION-MultiModelComparison.md (Detailed execution plan spec)
- Modify: None
- Read-Only: docs/vision.md, README.md, promptops/schemas/run-request.schema.json, promptops/schemas/scorecard.schema.json

3. Implementation Spec
- Harness Architecture: The harness adapter interface and plugin discovery remain unchanged. The runner shim will coordinate running the adapter multiple times (once per model) based on the run request.
- Run Request Format: Requires support for an array of model configurations instead of a single model config.
- Run Artifact Format: The scorecard will include a new top-level field `model_comparison` containing per-model breakdowns, deltas, and tradeoff surfaces (cost vs quality vs latency). Per-case records will include predictions and metrics from each model.
- Pseudo-Code:
  - Read run request
  - For each model config in run request:
    - Execute harness adapter
    - Collect cases.jsonl, failures.json
  - Run normalize.py with multi-model support enabled
    - Aggregate metrics per model
    - Compute tradeoff surface deltas between models
  - Output multi-model scorecard.json and merged cases.jsonl
- Baseline and Regression Flow: Baselines will be scoped to a specific model. Regression comparisons will compare against the baseline for the same model, or optionally compare a new model candidate against an old model baseline.
- Dependencies: CONTRACTS schemas (run-request, scorecard) need updating to support array of model configs and model_comparison scorecard fields. RUNTIME resolver must support multi-model evaluation execution.

4. Test Plan
- Verification: Execute the runner shim with a multi-model run request and verify the output artifacts.
- Success Criteria: A `scorecard.json` is produced containing a `model_comparison` block with accurate metrics and tradeoff deltas for each tested model.
- Edge Cases: One model fails while others succeed, models have different cost/latency structures, non-deterministic scores across models.
