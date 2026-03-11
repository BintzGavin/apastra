#### 1. Context & Goal
- **Objective**: Define the run artifact generation architecture for separating small indexes from large raw outputs.
- **Trigger**: `README.md` requires the generation of a durable output containing a manifest, scorecard, per-case records, raw artifact refs, and failures. It specifies that these run artifacts must be immutable, and structurally separated into small indexes in Git and large raw outputs referenced by digest in an external backend.
- **Impact**: Unlocks the ability to handle large scale evaluations without bloating the main git repository, while maintaining reproducibility.

#### 2. File Inventory
- **Create**: A bash script in `promptops/runs/` to handle artifact generation splitting
- **Modify**: `docs/status/EVALUATION.md`
- **Read-Only**: `README.md`, `promptops/schemas/run-artifact.schema.json`, `promptops/schemas/run-manifest.schema.json`, `promptops/schemas/run-case.schema.json`, `promptops/schemas/run-failures.schema.json`

#### 3. Implementation Spec
- **Harness Architecture**: The harness adapter will be configured to output to a temporary staging directory instead of the final `promptops/runs/` directory.
- **Run Request Format**: N/A
- **Run Artifact Format**: The monolithic `run_artifact.json` will be split into smaller, append-friendly index files: `run_manifest.json`, `scorecard.json`, `cases.jsonl`, `artifact_refs.json`, and `failures.json`.
- **Pseudo-Code**:
  1. Run the harness adapter targeting a temporary output directory.
  2. Read the generated `run_artifact.json` from the temporary directory.
  3. Extract the `manifest` object and write it to `run_manifest.json`.
  4. Extract the `scorecard` object and write it to `scorecard.json`.
  5. Extract the `cases` array, convert to JSONL format, and write to `cases.jsonl`.
  6. Extract any failures and write to `failures.json`.
  7. Generate a content digest for any large raw text or traces in the staging directory.
  8. Write an `artifact_refs.json` file mapping external artifact URIs to their computed digests.
  9. Move the split files to the final `runs/` directory or artifacts branch.
- **Baseline and Regression Flow**: Ensure the split `scorecard.json` is still accessible for the regression comparison engine.
- **Dependencies**: CONTRACTS schemas (`promptops/schemas/run-manifest.schema.json`, `promptops/schemas/run-case.schema.json`, `promptops/schemas/run-failures.schema.json`, `promptops/schemas/artifact-refs.schema.json`).

#### 4. Test Plan
- **Verification**:
  ```bash
  mkdir -p test-fixtures/run-artifact-test
  cat << 'JSON' > test-fixtures/run-artifact-test/dummy_run_manifest.json
  {
    "input_refs": {},
    "resolved_digests": {},
    "timestamps": {},
    "harness_version": "1.0",
    "model_ids": [],
    "environment": {},
    "status": "success"
  }
  JSON
  npx --yes ajv-cli validate -s promptops/schemas/run-manifest.schema.json -d test-fixtures/run-artifact-test/dummy_run_manifest.json --spec=draft2020 --strict=false -c ajv-formats
  ```
- **Success Criteria**:
  ```bash
  [ $? -eq 0 ]
  ```
- **Edge Cases**: Missing fields in the generated `run_artifact.json`, failures during file I/O operations.
