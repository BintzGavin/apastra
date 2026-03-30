#### 1. Context & Goal
- **Objective**: Implement red-team adversarial test case generation.
- **Trigger**: "Red-team adversarial generation" from `docs/vision.md`
- **Impact**: Provides automated adversarial inputs to evaluate prompt robustness against prompt injections, edge cases, multilingual inputs, and formatting breaks.

#### 2. File Inventory
- **Create**: None
- **Modify**: `promptops/runs/generate_adversarial_cases.py` (Update CLI script to generate adversarial datasets), `docs/status/EVALUATION.md` (Update version), `docs/progress/EVALUATION.md` (Add completion entry).
- **Read-Only**: `docs/vision.md`, `README.md`.

#### 3. Implementation Spec
- **Harness Architecture**: A standalone Python CLI tool that takes a prompt spec as input and generates an adversarial JSONL dataset.
- **Run Request Format**: N/A
- **Run Artifact Format**: N/A
- **Pseudo-Code**:
  1. Load prompt spec (YAML/JSON).
  2. If variables exist, iterate over them and generate adversarial cases:
     - Prompt injection (`IGNORE ALL PREVIOUS INSTRUCTIONS`)
     - Empty string
     - Multilingual string (`こんにちは世界`)
     - Format breaker (malformed JSON snippet)
  3. Output cases with `not-contains` or similar assertions in JSONL format.
- **Baseline and Regression Flow**: N/A.
- **Dependencies**: Depends on CONTRACTS relevant schemas.

#### 4. Test Plan
- **Verification**: Run `python promptops/runs/generate_adversarial_cases.py sample_spec.yaml test.jsonl` and verify output file is non-empty.
- **Success Criteria**: The `test.jsonl` contains valid JSON lines with adversarial strings mapped to prompt variables.
- **Edge Cases**: Prompt spec with no variables.
