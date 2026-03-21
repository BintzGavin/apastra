#### 1. Context & Goal
- **Objective**: Spec for implementing the `similar` assertion type in the deterministic evaluation engine.
- **Trigger**: The docs/vision.md lists `similar` as a model-assisted assertion type for semantic similarity, but `evaluate_assertions.py` currently hardcodes it to `True`.
- **Impact**: Enables actual semantic similarity checks to be integrated directly into deterministic eval runs, allowing pipelines to automatically gate merges on qualitative rubrics without requiring a separate platform.

#### 2. File Inventory
- **Create**:
  - None
- **Modify**:
  - `promptops/runs/evaluate_assertions.py` - Implement `similar` assertion logic.
- **Read-Only**:
  - `promptops/schemas/dataset-case.schema.json`
  - `docs/vision.md`
  - `promptops/schemas/run-request.schema.json`

#### 3. Implementation Spec
- **Harness Architecture**: The deterministic evaluation engine `evaluate_assertions.py` currently evaluates `answer-relevance` and `llm-rubric` by looking for a `judge_callable` in the `metadata` parameter. It calls this function with `(output, assert_value)` and expects a boolean or implicitly evaluates the result for truthiness. For `similar`, we will implement an identical pattern. `similar` will be removed from the `("similar", "factuality")` tuple that currently defaults to `True`.
- **Run Request Format**: No changes.
- **Run Artifact Format**: The `evaluator_outputs` for cases with `similar` assertions will reflect the returned boolean value as a float (`1.0` for `True`, `0.0` for `False`) instead of always being `1.0`.
- **Pseudo-Code**: High-level execution flow for `evaluate_assertions.py`:
  ```python
  elif base_type in ("answer-relevance", "llm-rubric", "similar"):
      if "judge_callable" in metadata:
          passed = metadata["judge_callable"](output, assert_value)
      elif assert_value:
          if isinstance(assert_value, list):
              passed = all(str(v).lower() in output.lower() for v in assert_value)
          else:
              passed = str(assert_value).lower() in output.lower()
      else:
          passed = True
  ```
- **Baseline and Regression Flow**: Regressions will now properly track changes in AI-graded scores.
- **Dependencies**: CONTRACTS schemas: `dataset-case.schema.json`. RUNTIME resolver: Required to execute the harness.

#### 4. Test Plan
- **Verification**: Run a minimal python script that imports `evaluate_assertions` and calls it with `assertions=[{"type": "similar", "value": "Is friendly"}]` and `metadata={"judge_callable": lambda o, v: True}`.
- **Success Criteria**: The output is `[{"assert_similar": 1.0}]` when the judge returns `True`, and `[{"assert_similar": 0.0}]` when the judge returns `False`.
- **Edge Cases**: Missing `judge_callable` falls back to substring match; invalid assertion type continues to fail gracefully.
