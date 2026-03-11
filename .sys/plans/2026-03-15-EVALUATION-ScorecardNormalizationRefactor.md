#### 1. Context & Goal
- **Objective**: Refactor the Scorecard Normalizer to read from `cases.jsonl` and output a distinct `scorecard.json` file.
- **Trigger**: The current normalization script (`promptops/runs/normalize.py`) mutates a monolithic artifact file in place, which violates the "append-friendly immutable artifacts" principle in README.md.
- **Impact**: Unlocks safe, immutable generation of scorecards for the separated artifact topology on the `promptops-artifacts` branch, supporting downstream GOVERNANCE checks.

#### 2. File Inventory
- **Create**: None
- **Modify**: `promptops/runs/normalize.py` (Refactor to accept input and output file paths, reading from JSONL and writing JSON).
- **Read-Only**: `README.md` (append-friendly immutable artifacts), `promptops/schemas/scorecard.schema.json` (expected output shape).

#### 3. Implementation Spec
- **Harness Architecture**: The normalizer acts as a post-processing step for harnesses. It must not modify its inputs.
- **Run Request Format**: N/A
- **Run Artifact Format**: The normalizer must read a standard `cases.jsonl` file line by line to extract evaluator outputs, then compute aggregate normalized metrics. It must output exactly one `scorecard.json` file conforming to the scorecard schema.
- **Pseudo-Code**:
  - Parse CLI args: `<cases.jsonl>` `<output_scorecard.json>`
  - Initialize empty metrics trackers.
  - Open `cases.jsonl` for reading.
  - For each line, parse JSON. Extract `evaluator_outputs`.
  - Accumulate metric sums and counts.
  - Compute averages and build `normalized_metrics` and `metric_definitions`.
  - Write output JSON object to `<output_scorecard.json>`.
- **Baseline and Regression Flow**: This distinct `scorecard.json` output will be directly read by the regression engine for candidate vs baseline comparison.
- **Dependencies**: CONTRACTS: `scorecard.schema.json`, `run-case.schema.json`.

#### 4. Test Plan
- **Verification**: Run `python promptops/runs/normalize.py test-fixtures/mock-cases.jsonl test-fixtures/mock-scorecard.json` and validate the output against the schema using `npx --yes ajv-cli validate -s promptops/schemas/scorecard.schema.json -d test-fixtures/mock-scorecard.json`.
- **Success Criteria**: The script creates `test-fixtures/mock-scorecard.json` without modifying `test-fixtures/mock-cases.jsonl`, and validation passes.
- **Edge Cases**: Empty cases file, missing evaluator outputs in cases, zero values.
