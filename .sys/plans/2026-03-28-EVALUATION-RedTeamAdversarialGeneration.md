#### 1. Context & Goal
- **Objective**: Implement red-team adversarial test case generation.
- **Trigger**: docs/vision.md explicitly lists "Red-team adversarial generation" (Priority 9) as a feature, which requires generating adversarial test cases (prompt injection attempts, edge-case inputs, multilingual stress tests, format-breaking inputs) for a given prompt spec.
- **Impact**: Enables teams to harden their prompts against adversarial inputs and edge cases, improving prompt robustness and security.

#### 2. File Inventory
- **Create**: promptops/runs/generate_adversarial_cases.py
- **Modify**: None
- **Read-Only**: docs/vision.md

#### 3. Implementation Spec
- **Harness Architecture**: Spec a new utility script generate_adversarial_cases.py that takes a prompt spec as input and generates a dataset of adversarial test cases. The script uses an LLM (acting as the "Adversarial QA" role) to generate inputs designed to break the prompt's instructions or output contract.
- **Run Request Format**: Output dataset will be referenced in standard run requests.
- **Run Artifact Format**: The output is a standard JSONL dataset file containing the generated adversarial inputs and expected assertion failures or boundary conditions.
- **Pseudo-Code**:
  ```python
  import sys
  import json
  # Load prompt spec
  # Construct meta-prompt for Adversarial QA generation
  # Call LLM to generate adversarial inputs
  # Format as dataset-case.schema.json objects
  # Write to output JSONL file
  ```
- **Dependencies**: Requires an LLM integration for generation.

#### 4. Test Plan
- **Verification**: Run python promptops/runs/generate_adversarial_cases.py test-prompt.yaml output-dataset.jsonl
- **Success Criteria**: A valid JSONL dataset file is generated containing test cases designed to break the target prompt.
- **Edge Cases**: Handling prompts with no variables, ensuring generated cases cover different attack vectors.
