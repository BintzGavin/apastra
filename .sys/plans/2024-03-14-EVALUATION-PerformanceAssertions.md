#### 1. Context & Goal
- **Objective**: Implement performance assertions (`latency` and `cost`) in the deterministic evaluation engine.
- **Trigger**: The `docs/vision.md` explicitly lists `latency` and `cost` as supported performance assertions, but they are currently hardcoded to always pass in `evaluate_assertions.py`.
- **Impact**: Enables regression policies and scorecard thresholds to reliably gate runs based on token cost and response time, fulfilling the complete assertion vocabulary.

#### 2. File Inventory
- **Create**: None
- **Modify**: `promptops/runs/evaluate_assertions.py`, `promptops/harnesses/reference-adapter/run.py`
- **Read-Only**: `docs/vision.md`

#### 3. Implementation Spec
- **Harness Architecture**: Update the `evaluate_assertions` function to accept an optional `metadata` dictionary containing execution details like latency and token cost. Update the reference adapter to pass these values when calling the function.
- **Run Request Format**: N/A
- **Run Artifact Format**: N/A
- **Pseudo-Code**:
  - Modify `evaluate_assertions(output: str, assertions: list, metadata: dict = None) -> list`.
  - For `latency` assertions, compare `metadata.get("latency", 0)` to the `assert_value`. The threshold implies `value <= assert_value` passes.
  - For `cost` assertions, compare `metadata.get("cost", 0.0)` to the `assert_value`. The threshold implies `value <= assert_value` passes.
  - Update `promptops/harnesses/reference-adapter/run.py` to provide a mock `metadata` dictionary with `latency` and `cost` when calling `evaluate_assertions`.
- **Baseline and Regression Flow**: N/A
- **Dependencies**: N/A

#### 4. Test Plan
- **Verification**: `python -c "import sys; sys.path.insert(0, 'promptops/runs'); from evaluate_assertions import evaluate_assertions; print(evaluate_assertions('test', [{'type': 'latency', 'value': 100}], {'latency': 50}))"`
- **Success Criteria**: The function correctly evaluates latency and cost assertions based on provided metadata, returning 1.0 for pass and 0.0 for fail.
- **Edge Cases**: Missing metadata (defaults to fail), invalid threshold types, negated assertions.