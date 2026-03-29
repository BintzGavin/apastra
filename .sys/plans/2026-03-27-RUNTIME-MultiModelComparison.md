#### 1. Context & Goal
- **Objective**: Implement a Multi-Model Comparison workflow in the runtime.
- **Trigger**: Expansion 3 in `docs/vision.md` and `README.md` describes a missing multi-model comparison experience to help teams compare prompts across N models and generate a comparison scorecard.
- **Impact**: Unlocks the ability for teams to systematically evaluate prompts across different models side-by-side, assessing cost, quality, and latency tradeoffs to make informed promotion decisions.

#### 2. File Inventory
- **Create**:
  - `promptops/runtime/compare.py`: Core logic for executing a suite across multiple models and generating a comparison scorecard.
- **Modify**:
  - `promptops/runtime/cli.py`: Add a new `compare` command to invoke the multi-model comparison workflow.
  - `promptops/runtime/__init__.py`: Add imports to expose the multi-model functionality.
- **Read-Only**:
  - CONTRACTS schemas for comparison scorecards, suites, and run requests.
  - `docs/vision.md`: To adhere to the specific multi-model comparison workflow requirements.

#### 3. Implementation Spec
- **Resolver Architecture**:
  - The compare workflow will take a suite ID and an optional list of model IDs to override the suite's `model_matrix`.
  - It will construct a run request for each model in the matrix.
  - It will invoke the `runner.py` logic (or a refactored version of it) for each model.
  - It will collect the individual `scorecard.json` outputs from each run.
  - It will aggregate these individual scorecards into a single `comparison_scorecard.json` that includes per-model breakdowns and cost/quality/latency tradeoffs.
- **Manifest Format**:
  - N/A for this specific task, as it primarily interacts with suites and scorecards.
- **Pseudo-Code**:
  ```python
  def run_comparison(suite_id, models=None):
      suite = load_suite(suite_id)
      models_to_run = models or suite.get("model_matrix", ["default"])

      individual_scorecards = {}
      for model in models_to_run:
          run_req = construct_run_request(suite, model)
          out_dir = run_harness(run_req)
          individual_scorecards[model] = load_scorecard(out_dir)

      comparison_scorecard = generate_comparison(individual_scorecards)
      validate_against_schema(comparison_scorecard, "relevant schema")
      return comparison_scorecard
  ```
- **Harness Contract Interface**:
  - The runtime will interact with the harness adapter by generating specific `run_request.json` files for each model and expecting standard `scorecard.json` files in the output directory.
- **Dependencies**:
  - Relevant CONTRACTS schemas.

#### 4. Test Plan
- **Verification**: Run `python promptops/runtime/cli.py compare my-suite --models modelA modelB`.
- **Success Criteria**:
  - The command successfully runs the suite against both models.
  - A `comparison_scorecard.json` is generated and outputted.
  - The generated scorecard passes validation against the relevant schema.
- **Edge Cases**:
  - A suite with no `model_matrix` and no models provided via CLI.
  - Harness execution failure for one or more models.
  - Invalid scorecard returned by the harness.
