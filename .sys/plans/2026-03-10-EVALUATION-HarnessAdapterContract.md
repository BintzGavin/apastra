#### 1. Context & Goal
- **Objective**: Define the harness adapter contract, run request format, and run artifact format.
- **Trigger**: The README.md specifies a "Harness adapter contract" (run request in -> run artifact out) but `promptops/harnesses/` and `promptops/runs/` lack an explicit contract.
- **Impact**: This unlocks the ability to build and run multiple interchangeable harnesses (e.g. Python, JS, Promptfoo) without rewriting source-of-truth concepts. It unblocks the Run Artifact generation, Scorecard normalization, Baseline creation, and Regression policy evaluations which depend on the adapter output.

#### 2. File Inventory
- **Create**:
  - `promptops/schemas/harness-adapter.schema.json` (Contract schema defining how an adapter config is specified)
  - `promptops/schemas/run-request.schema.json` (Schema defining the input work order)
  - `promptops/schemas/run-artifact.schema.json` (Schema defining the durable output directory contents, including manifest, scorecard, and cases)
- **Modify**: []
- **Read-Only**:
  - `promptops/schemas/suite.schema.json`
  - `promptops/schemas/prompt-spec.schema.json`
  - `README.md` (Harness Adapter Contract, Run Request, Run Artifact sections)

#### 3. Implementation Spec
- **Harness Architecture**:
  - The harness adapter acts as a wrapper around an evaluation framework (e.g., promptfoo, custom python script).
  - **Interface**: Executable that takes a path to a `run_request.json` as the single input argument and writes the output to a specified directory.
  - **Plugin Discovery**: Adapters are registered in the `promptops/harnesses/` directory with a `.yaml` or `.json` file matching the `harness-adapter.schema.json`.
  - **Error Contract**: The harness must return a non-zero exit code on framework failure. Output errors in evaluations should be recorded in the `failures.json` or `scorecard.json` rather than crashing the harness.
- **Run Request Format**:
  - Required fields: `suite_id`, `revision_ref` (digest/sha), `model_matrix` (list of models), `samplers` (temperature, max_tokens), `evaluator_refs`, `output_dir`.
- **Run Artifact Format**:
  - Append-only directory containing:
    - `run_manifest.json`: Metadata, input digests, harness version, timestamps.
    - `scorecard.json`: Normalized metrics summary per run.
    - `cases.jsonl`: Per-case execution results, stable `case_id`s, evaluator outputs.
    - `artifact_refs.json`: Pointers to large outputs (logs/traces).
    - `failures.json`: Structured list of failures.
- **Pseudo-Code**:
  ```python
  # Pseudo-code for a harness adapter wrapper
  def run_harness(run_request_path: str):
      request = load_json(run_request_path)

      # Dependencies
      prompts = RUNTIME_resolver(request.revision_ref)
      suite = load_suite(request.suite_id)

      results = execute_eval_framework(prompts, suite, request.model_matrix)

      write_artifact(request.output_dir, results)
  ```
- **Dependencies**:
  - **CONTRACTS**: Requires `harness-adapter.schema.json`, `run-request.schema.json`, `run-artifact.schema.json` from the CONTRACTS domain.
  - **RUNTIME**: The harness relies on a RUNTIME resolver to resolve `revision_ref` to concrete prompt spec files before execution.

#### 4. Test Plan
- **Verification**: Run `ajv-cli` to validate dummy `harness-adapter.yaml`, `run-request.json`, and `run-artifact` files against the newly created schemas.
- **Success Criteria**:
  - The schema correctly requires the specified input fields for a run request.
  - The schema correctly requires the specified output fields in the run artifact.
- **Edge Cases**:
  - Missing output directory in run request.
  - Framework crash handling (ensure non-zero exit).
  - Invalid evaluator references.