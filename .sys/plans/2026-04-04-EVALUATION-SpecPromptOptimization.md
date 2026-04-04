#### 1. Context & Goal
- **Objective**: Spec the prompt optimization capability.
- **Trigger**: `docs/vision.md` and `README.md` list "Prompt optimization" (apastra-optimize skill) as a planned feature to analyze token usage, suggest compression, and estimate cost reduction.
- **Impact**: Unlocks the ability for teams to reduce their inference costs by compressing prompts without losing evaluation performance.

#### 2. File Inventory
- **Create**: `promptops/schemas/prompt-optimization-report.schema.json` (Schema for optimization outputs), `promptops/harnesses/optimization-analyzer.py` (Script to run the token analysis and cost estimation).
- **Modify**: None.
- **Read-Only**: []

#### 3. Implementation Spec
- **Harness Architecture**: The `optimization-analyzer.py` is an independent utility script that loads a prompt spec and a run manifest. It calculates the base token usage, identifies instructions that could be compressed (e.g., redundant phrases), and produces an optimization report. It does not run evaluations itself, but reads outputs from a harness run.
- **Run Request Format**: Uses the existing `run-request.schema.json`, plus additional metadata for token price references (e.g., input cost per 1M tokens).
- **Run Artifact Format**: The output is an `OptimizationReport` that contains original token counts, estimated compressed token counts, estimated dollar savings across a large number of invocations (e.g., 1M runs), and specific text span compression suggestions.
- **Pseudo-Code**:
  1. Load prompt spec and run manifest.
  2. Read total token usage from the manifest.
  3. Apply heuristic token compression rules (e.g., whitespace removal, synonym replacement, instruction condensation) to the prompt template.
  4. Recalculate token count for the new template.
  5. Calculate cost difference = (original_tokens - new_tokens) * price_per_token * 1M invocations.
  6. Output JSON optimization report.
- **Baseline and Regression Flow**: Optimization runs can be used to generate a new prompt variant. The new variant can then be evaluated against the baseline to ensure quality did not regress despite the token reduction.
- **Dependencies**: Depends on existing RUNTIME resolver for loading the prompt and EVALUATION harness for providing the initial run manifest.

#### 4. Test Plan
- **Verification**: Run `python3 promptops/harnesses/optimization-analyzer.py --prompt prompt.yaml --manifest run_manifest.json --out report.json` on a sample set of files.
- **Success Criteria**: A valid `report.json` is generated containing `original_tokens`, `compressed_tokens`, `cost_savings_estimate`, and `compression_suggestions`, successfully validating against `prompt-optimization-report.schema.json`.
