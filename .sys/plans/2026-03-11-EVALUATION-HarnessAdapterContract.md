#### 1. Context & Goal
- **Objective**: Define the Harness Adapter Contract implementation spec to bridge run requests to run artifacts.
- **Trigger**: `README.md` mandates a minimal BYO harness interface (run request in → run artifact out), but `promptops/harnesses/` only contains an empty directory, and no reference implementation or execution protocol exists.
- **Impact**: Unlocks the ability to execute benchmark suites by providing a concrete, schema-compliant adapter implementation. This enables the Run Artifact generation phase, which is required for scorecard normalization and regression reporting.

#### 2. File Inventory
- **Create**: A reference harness adapter configuration file (YAML) declaring capabilities and entrypoint.
- **Create**: A minimal reference adapter script to process a run request, resolve prompts using RUNTIME, and emit a compliant run artifact.
- **Modify**: None
- **Read-Only**: `promptops/schemas/harness-adapter.schema.json`, `promptops/schemas/run-request.schema.json`, `promptops/schemas/run-artifact.schema.json`, `promptops/runtime/resolve.py`, `README.md`

#### 3. Implementation Spec
- **Harness Architecture**: The harness adapter is invoked as a stateless worker. It receives a path to a run request and an output directory. It must declare its capabilities in a YAML configuration (e.g., `run_suite`). Errors must be caught and recorded in the `failures` array of the run artifact rather than crashing silently.
- **Run Request Format**: Consumes `suite_id`, `revision_ref`, `model_matrix`, and `evaluator_refs` as defined in `promptops/schemas/run-request.schema.json`.
- **Run Artifact Format**: Produces `manifest`, `scorecard`, `cases`, and `failures` objects matching `promptops/schemas/run-artifact.schema.json` within the specified output directory.
- **Pseudo-Code**:
  1. Parse the run request JSON from input args.
  2. Invoke `promptops/runtime/resolve.py` for the `revision_ref` to materialize the prompt.
  3. Initialize output directory structures.
  4. Iterate through `model_matrix` and test cases.
  5. Write `manifest`, `scorecard`, `cases`, and `failures` JSON data to the output directory.
- **Baseline and Regression Flow**: N/A for this scope (handled post-run).
- **Dependencies**: CONTRACTS schemas (`promptops/schemas/run-request.schema.json`, `promptops/schemas/run-artifact.schema.json`, `promptops/schemas/harness-adapter.schema.json`), RUNTIME resolver (`promptops/runtime/resolve.py`).

#### 4. Test Plan
- **Verification**: Verify the implementation logic produces a schema-compliant artifact.
  `mkdir -p test-fixtures/harness-test`
  `echo '{"suite_id":"test-suite","revision_ref":"main","model_matrix":["model-1"],"evaluator_refs":["eval-1"]}' > test-fixtures/harness-test/request.json`
  `# The executor must replace [YOUR_ADAPTER_COMMAND] with the entrypoint command for their created adapter`
  `[YOUR_ADAPTER_COMMAND] test-fixtures/harness-test/request.json test-fixtures/harness-test/out.json`
  `npx ajv-cli validate -s promptops/schemas/run-artifact.schema.json -d test-fixtures/harness-test/out.json --spec=draft2020 --strict=false`
- **Success Criteria**:
  `[ $? -eq 0 ]`
- **Edge Cases**: Empty test cases, resolver failures, schema validation of outputs.
