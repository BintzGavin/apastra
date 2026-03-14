#### 1. Context & Goal
- **Objective**: Implement deterministic inline assertions evaluation engine.
- **Trigger**: `docs/vision.md` defines "Inline assertions" and "Built-in assertion types" (e.g., equals, contains, regex), but harness execution currently mocks all assertions to 1.0.
- **Impact**: Unlocks real gating and regression detection by accurately evaluating cases against expected assertions.

#### 2. File Inventory
- **Create**: `promptops/runs/evaluate_assertions.py` (Script to evaluate actual deterministic assertions against output).
- **Modify**: `promptops/harnesses/reference-adapter/run.py` (Integrate the evaluation script to calculate real assertion scores instead of mock 1.0).
- **Read-Only**: `promptops/schemas/evaluator.schema.json`, `docs/vision.md` (Built-in assertion types).

#### 3. Implementation Spec
- **Harness Architecture**: Adapter will invoke `evaluate_assertions.py` for each case's generated output and list of inline assertions.
- **Run Request Format**: `dataset_path` containing cases with inline `assert` arrays.
- **Run Artifact Format**: `evaluator_outputs` in `cases.jsonl` will contain real 1.0 (pass) or 0.0 (fail) scores for each assertion type.
- **Pseudo-Code**:
  - `evaluate_assertions.py` reads a single output string and an array of assertions.
  - Maps assertion types (`equals`, `contains`, `icontains`, `regex`, `starts-with`, `is-json`, `contains-json`) to python logic.
  - Returns a dict of `{"assert_<type>": score}`.
  - `run.py` calls this logic after generating `mock_output` (or real output if integrated with provider).
- **Baseline and Regression Flow**: Improved accuracy in scorecards feeds the existing regression engine.
- **Dependencies**: CONTRACTS `evaluator.schema.json`. RUNTIME `resolve` utility.

#### 4. Test Plan
- **Verification**: `python promptops/harnesses/reference-adapter/run.py dummy_request.json out_dir` using a mock request with inline assertions.
- **Success Criteria**: `cases.jsonl` in `out_dir` contains `evaluator_outputs` accurately reflecting the assertion logic (e.g., 0.0 for failing assertions).
- **Edge Cases**: Output missing, invalid regex pattern, invalid JSON.
