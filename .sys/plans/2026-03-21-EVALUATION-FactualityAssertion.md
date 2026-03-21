#### 1. Context & Goal
- **Objective**: Spec for implementing the `factuality` assertion type in the deterministic evaluation engine.
- **Trigger**: The docs/vision.md lists `factuality` as a model-assisted assertion type that "Checks output against reference facts", but `evaluate_assertions.py` currently hardcodes it to `True`.
- **Impact**: Enables actual factuality checks to be integrated directly into deterministic eval runs, allowing pipelines to automatically gate merges on factual correctness rubrics.

#### 2. File Inventory
- **Create**:
  - None
- **Modify**:
  - `promptops/runs/evaluate_assertions.py` - Implement `factuality` assertion logic.
- **Read-Only**:
  - `promptops/schemas/dataset-case.schema.json`
  - `docs/vision.md`
  - `promptops/schemas/run-request.schema.json`

#### 3. Implementation Spec
- **Harness Architecture**: The deterministic evaluation engine `evaluate_assertions.py` currently evaluates `answer-relevance`, `llm-rubric`, and `similar` by looking for a `judge_callable` in the `metadata` parameter. It calls this function with `(output, assert_value)` and expects a boolean. For `factuality`, we will follow this same pattern. We'll update `evaluate_assertions.py` to add `factuality` to the list of assertions that use `judge_callable`.
- **Run Request Format**: No changes.
- **Run Artifact Format**: The `evaluator_outputs` for cases with `factuality` assertions will reflect the returned boolean value as a float (`1.0` for `True`, `0.0` for `False`) instead of always being `1.0`.
- **Pseudo-Code**: High-level execution flow for `evaluate_assertions.py`:
  ```python
  elif base_type in ("answer-relevance", "llm-rubric", "similar", "factuality"):
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
- **Baseline and Regression Flow**: Regressions will now properly track changes in factuality scores.
- **Dependencies**: CONTRACTS schemas required: `dataset-case.schema.json`. RUNTIME resolver availability: Required to execute the harness. GOVERNANCE policy files needed: None.

#### 4. Test Plan
- **Verification**: Run a minimal python script that imports `evaluate_assertions` and calls it with `assertions=[{"type": "factuality", "value": "Paris is the capital of France"}]` and `metadata={"judge_callable": lambda o, v: True}`.
- **Success Criteria**: The output is `[{"assert_factuality": 1.0}]` when the judge returns `True`, and `[{"assert_factuality": 0.0}]` when the judge returns `False`.
- **Edge Cases**: Missing `judge_callable` falls back to substring match; invalid assertion type continues to fail gracefully.
