#### 1. Context & Goal
- **Objective**: Implement support for "Quick Eval Mode" in the run pipeline.
- **Trigger**: `docs/vision.md` and `README.md` describe a rapid iteration mode using a single file (`promptops/evals/my-eval.yaml`), but the current `promptops/runs/` implementation does not support executing or resolving it.
- **Impact**: Enables rapid iteration by allowing developers to write prompts, test cases, and assertions in a single file without setting up the full suite/evaluator/dataset file structure.

#### 2. File Inventory
- **Create**: `promptops/runs/quick-eval.sh` (Entry point for converting a quick eval file into a standard run request and artifact pipeline).
- **Modify**: `promptops/harnesses/reference-adapter/run.py` (Add parsing logic for inline assertions and quick eval mode).
- **Read-Only**: `docs/vision.md`, `README.md`, `promptops/schemas/run-request.schema.json`.

#### 3. Implementation Spec
- **Harness Architecture**: A `promptops/runs/quick-eval.sh` script reads the YAML from `promptops/evals/` and dynamically scaffolds a temporary standard run request and dataset. The reference adapter `promptops/harnesses/reference-adapter/run.py` is updated to process inline assertions attached to cases.
- **Run Request Format**: Quick eval mode abstracts away the run request format, generating a temporary standard `run_request.json` pointing to a temporary `.jsonl` dataset with inline assert objects.
- **Run Artifact Format**: Output scorecard and cases JSONL follow the same append-friendly schema as regular suites.
- **Pseudo-Code**:
  1. Read `promptops/evals/<id>.yaml`.
  2. Extract prompt template, cases, and assertions.
  3. Generate a dynamic `run_request.json` and a temporary `.jsonl` dataset with inline assert objects.
  4. Pass to the reference adapter `run.py`.
  5. Clean up temporary files after execution.
- **Baseline and Regression Flow**: Uses standard flow against the generated scorecard.
- **Dependencies**: CONTRACTS must establish schema definitions for quick eval yaml structures. RUNTIME resolver must handle inline prompts.

#### 4. Test Plan
- **Verification**: Run `bash promptops/runs/quick-eval.sh promptops/evals/test-eval.yaml` to verify the execution pipeline produces a valid run artifact.
- **Success Criteria**: A quick eval file in `promptops/evals/` successfully produces `scorecard.json` when run through the quick eval pipeline.
- **Edge Cases**: Missing assertions, malformed YAML structure, missing variables in prompt template.
