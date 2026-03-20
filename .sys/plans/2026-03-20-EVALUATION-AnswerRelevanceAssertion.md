#### 1. Context & Goal
- **Objective**: Implement the `answer-relevance` model-assisted inline assertion.
- **Trigger**: The vision docs and dataset schemas define `answer-relevance` as a built-in model-assisted assertion type, but `promptops/runs/evaluate_assertions.py` currently just returns a placeholder `True` for it.
- **Impact**: Enables deterministic and automated evaluation of output relevance using standard harness executions.

#### 2. File Inventory
- **Create**: None
- **Modify**: `promptops/runs/evaluate_assertions.py`
- **Read-Only**: `promptops/schemas/dataset-case.schema.json`, `docs/vision.md`, `README.md`

#### 3. Implementation Spec
- **Harness Architecture**: Model-assisted evaluation built into the deterministic assertions engine.
- **Run Request Format**: No changes.
- **Run Artifact Format**: No changes.
- **Pseudo-Code**:
  - In `evaluate_assertions.py`, locate the `answer-relevance` check inside `evaluate_assertions`.
  - Modify the logic to use a provided LLM/model callable (or assume one from context) to score the text for relevance against an input or reference value.
  - Since `evaluate_assertions.py` is currently a synchronous, non-model-aware script, the real implementation will either need a passed-in judge model or will mock the return until full LLM rubric judging is wired into the harness adapter layer. For now, the implementation should attempt to calculate string similarity or rely on the `value` field containing expected keywords if a judge model is unavailable.
- **Baseline and Regression Flow**: Allows baseline establishment for answer relevance scores.
- **Dependencies**: RUNTIME python resolver must exist to parse datasets.

#### 4. Test Plan
- **Verification**: Run `python -m pytest` or `python promptops/runs/evaluate_assertions.py` against a sample inline assertion.
- **Success Criteria**: The function successfully evaluates an `answer-relevance` assertion and returns a float score or boolean based on the actual relevance calculation instead of always returning `True`.
- **Edge Cases**: No reference value provided, output is completely unrelated, negated `not-answer-relevance` assertions.
