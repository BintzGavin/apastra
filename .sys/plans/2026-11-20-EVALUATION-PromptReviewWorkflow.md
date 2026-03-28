#### 1. Context & Goal
- **Objective**: Spec a role-based agent skill "Prompt Review Workflow" to analyze prompt specs.
- **Trigger**: The docs/vision.md defines an expansion feature: "Prompt review" that acts as a "Paranoid staff prompt engineer" reviewing specs for ambiguity, injection surface, variable hygiene, and output contract completeness.
- **Impact**: Unlocks automated prompt review to catch foundational prompt issues before evaluation suites are run, improving prompt safety and quality upfront.

#### 2. File Inventory
- **Create**: promptops/evals/prompt-review-eval.yaml
- **Modify**: None
- **Read-Only**: promptops/schemas/prompt-spec.schema.json, docs/vision.md

#### 3. Implementation Spec
- **Harness Architecture**: N/A
- **Run Request Format**: The prompt spec itself acts as the input to an LLM evaluator that asserts its structure and contents.
- **Run Artifact Format**: Scorecard with assertions evaluating injection surface and ambiguity.
- **Pseudo-Code**:
  # Create quick-eval file promptops/evals/prompt-review-eval.yaml
  # Define a prompt template that takes the target prompt spec content as input
  # Provide assertion logic using llm-rubric for "ambiguity", "injection surface", "variable hygiene"
  # Require a pass_rate threshold to pass the review
- **Baseline and Regression Flow**: The baseline is simply the first reviewed state; regressions flag new changes that introduce ambiguity or injection vulnerabilities.
- **Dependencies**: CONTRACTS must support quick eval schemas and llm-rubric assertions.

#### 4. Test Plan
- **Verification**: Run promptops/runs/quick-eval.sh promptops/evals/prompt-review-eval.yaml with a mock prompt spec to evaluate its rules.
- **Success Criteria**: The quick eval successfully loads the prompt spec, applies the rubric, and produces a valid run artifact with pass/fail on the prompt's quality.
- **Edge Cases**: Prompts with missing variables, extreme lengths, or complex JSON output schemas without sufficient descriptions.
