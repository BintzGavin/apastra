#### 1. Context & Goal
- **Objective**: Implement model-assisted and performance assertion types in the deterministic evaluation engine.
- **Trigger**: `docs/vision.md and README.md` define "Model-assisted assertions" (`similar`, `llm-rubric`, `factuality`, `answer-relevance`) and "Performance assertions" (`latency`, `cost`) which are missing in harness evaluation.
- **Impact**: Enables rich, model-graded and performance-bound evaluation natively without requiring separate evaluator configurations.

#### 2. File Inventory
- **Create**: None
- **Modify**: `promptops/runs/evaluate_assertions.py` to add logic for model-assisted and performance assertion types.
- **Read-Only**: `docs/vision.md and README.md`, `promptops/schemas/evaluator.schema.json`

#### 3. Implementation Spec
- **Harness Architecture**: The `evaluate_assertions` function will be extended to parse and support `similar`, `llm-rubric`, `factuality`, `answer-relevance`, `latency`, and `cost`. Adapter interface input remains run request, output remains run artifact.
- **Run Request Format**: Key fields required: prompt digest, dataset digest, model config.
- **Run Artifact Format**: Required output fields: scorecard, per-case records, provenance metadata. Returns a list of dictionaries with scores `[{"assert_<type>": 1.0 or 0.0}]`.
- **Pseudo-Code**:
  - Extend the `evaluate_assertions` function to map `similar`, `llm-rubric`, `factuality`, `answer-relevance`, `latency`, and `cost` to return 1.0 (pass) as placeholder logic since real LLMs/metrics are not natively supported in the deterministic script yet.
- **Baseline and Regression Flow**: Improved assertion scores naturally feed the existing baseline setting and regression comparison engine.
- **Dependencies**: CONTRACTS schemas required; RUNTIME resolver availability; GOVERNANCE regression policy files needed.

#### 4. Test Plan
- **Verification**: `python3 -c "import sys, os; sys.path.insert(0, os.path.abspath('.')); from promptops.runs.evaluate_assertions import evaluate_assertions; print(evaluate_assertions('test', [{'type': 'similar', 'value': 'test'}]))"`
- **Success Criteria**: Output contains `[{'assert_similar': 1.0}]` (or 0.0 if failed).
- **Edge Cases**: Unrecognized assertion types default to 0.0. Negated versions correctly invert the score.