#### 1. Context & Goal
- **Objective**: Spec the specific implementations of `similar` and `factuality` assertion types.
- **Trigger**: `docs/vision.md` explicitly defines `similar` and `factuality` as model-assisted assertion types. However, `promptops/runs/evaluate_assertions.py` groups them with `answer-relevance` and `llm-rubric` and lacks a standalone implementation, instead relying on a placeholder or generic fallback. As with `answer-relevance` and `llm-rubric` (which needed explicit specs per `.jules/EVALUATION.md`), `similar` and `factuality` are remaining vision gaps that need their own dedicated logic specs to function natively.
- **Impact**: Enables fact-checking and semantic similarity checks in evaluation suites natively, as promised by the vision, ensuring model hallucinations and output drift are detected accurately.

#### 2. File Inventory
- **Create**: `.sys/plans/2026-04-01-EVALUATION-FactualityAndSimilarAssertions.md`
- **Modify**: N/A
- **Read-Only**: `docs/vision.md`, `promptops/runs/evaluate_assertions.py`

#### 3. Implementation Spec
- **Harness Architecture**: N/A
- **Run Request Format**: N/A
- **Run Artifact Format**: N/A
- **Pseudo-Code**:
  - Update `promptops/runs/evaluate_assertions.py` to separate `similar` and `factuality` from the generic fallback logic.
  - For `similar`, spec semantic similarity logic comparing output against the reference `assert_value` and threshold (e.g., using embedding cosine similarity or an LLM judge prompt).
  - For `factuality`, spec logic to check output against reference facts (e.g., using an LLM judge prompt with facts provided as `assert_value`).
- **Baseline and Regression Flow**: N/A
- **Dependencies**: RUNTIME resolver; GOVERNANCE policy files.

#### 4. Test Plan
- **Verification**: Run `python promptops/runs/evaluate_assertions.py` with mock assertions of type `similar` and `factuality`.
- **Success Criteria**: The function correctly evaluates these assertion types based on the new logic.
- **Edge Cases**: Missing judge configuration, invalid similarity threshold.
