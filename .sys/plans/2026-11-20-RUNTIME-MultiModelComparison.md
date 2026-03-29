#### 1. Context & Goal
- **Objective**: Implement a Multi-Model Comparison workflow in the runtime.
- **Trigger**: "Expansion 3: Multi-model comparison" in `docs/vision.md` calls for running a suite against N models simultaneously and generating a comparison scorecard.
- **Impact**: Unlocks the ability for teams to systematically evaluate prompts across different models side-by-side to assess cost, quality, and latency tradeoffs.

#### 2. File Inventory
- **Create**:
  - `promptops/runtime/compare.py`: Core logic for orchestrating a suite run across multiple models and aggregating the outputs into a comparison scorecard.
- **Modify**:
  - `promptops/runtime/cli.py`: Add a new `compare` subcommand to invoke the multi-model comparison workflow.
  - `promptops/runtime/__init__.py`: Export the multi-model comparison logic.
- **Read-Only**:
  - `promptops/schemas/comparison-scorecard.schema.json`
  - `promptops/schemas/run-request.schema.json`
  - `docs/vision.md`

#### 3. Implementation Spec
- **Resolver Architecture**: The compare workflow will take a suite ID and an optional list of model IDs to override the suite's `model_matrix`. It will construct individual run requests for each model, invoke the `runner.py` harness logic for each, collect the resulting `scorecard.json` files from their respective output directories, and aggregate them into a final `comparison_scorecard.json`.
- **Manifest Format**: N/A for this task.
- **Pseudo-Code**:
  ```python
  def run_comparison(suite_id, models=None):
      suite = load_suite(suite_id)
      models_to_run = models or suite.get("model_matrix", ["default"])
      individual_scorecards = {}
      for model in models_to_run:
          run_req = construct_run_request(suite, model)
          out_dir = invoke_harness(run_req)
          individual_scorecards[model] = load_scorecard(out_dir)
      comparison_scorecard = aggregate_scorecards(individual_scorecards)
      return comparison_scorecard
  ```
- **Harness Contract Interface**: The runtime interacts with the harness adapter by generating specific `run_request.json` files for each model and expecting standard `scorecard.json` files in the output directory.
- **Dependencies**: Depends on the existence of `comparison-scorecard.schema.json` in the CONTRACTS domain.

#### 4. Test Plan
- **Verification**: Run `python promptops/runtime/cli.py compare test-suite --models model-a model-b` and verify that a valid `comparison_scorecard.json` is generated.
- **Success Criteria**: The CLI command successfully orchestrates multiple harness runs, aggregates the metrics into a single comparison scorecard, and the output passes schema validation against `comparison-scorecard.schema.json`.
- **Edge Cases**: Suite lacks a `model_matrix` and no models are provided; harness execution fails for a subset of the models.
