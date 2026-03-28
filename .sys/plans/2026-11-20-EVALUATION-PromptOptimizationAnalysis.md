#### 1. Context & Goal
- **Objective**: Spec the prompt optimization analysis feature for the evaluation framework.
- **Trigger**: The docs/vision.md proposes "Prompt optimization: analyze a prompt's token usage, suggest compression techniques, identify unnecessary instructions, estimate cost reduction".
- **Impact**: Enables agents to run specialized prompt review and optimization passes on prompt specs before they are merged or benchmarked.

#### 2. File Inventory
- **Create**: promptops/evaluators/prompt-optimization-review.yaml
- **Modify**: None
- **Read-Only**: promptops/schemas/evaluator.schema.json, docs/vision.md

#### 3. Implementation Spec
- **Harness Architecture**: Uses standard harness execution, evaluating prompt text directly rather than model outputs.
- **Run Request Format**: Unchanged.
- **Run Artifact Format**: Unchanged.
- **Pseudo-Code**:
  # Create prompt-optimization-review.yaml evaluator
  # type: llm-rubric
  # rubric: "Evaluate the given prompt spec for token efficiency. 1. Identify repetitive instructions. 2. Suggest compression techniques. 3. Estimate cost reduction. 4. Score from 0.0 to 1.0 based on how optimized the prompt is."
- **Baseline and Regression Flow**: Unchanged.
- **Dependencies**: CONTRACTS domain must provide the evaluator schema.

#### 4. Test Plan
- **Verification**: Run `ajv-cli validate` against the new evaluator file using `promptops/schemas/evaluator.schema.json`.
- **Success Criteria**: The evaluator file passes schema validation.
- **Edge Cases**: Empty prompt specs, prompts that are already optimally compressed.
