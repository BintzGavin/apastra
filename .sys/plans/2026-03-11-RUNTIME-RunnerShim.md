#### 1. Context & Goal
- **Objective**: Implement the runner shim to invoke the harness adapter with a run request and collect the run artifact directory.
- **Trigger**: The README.md specifies "Implement runner shim: invoke harness adapter with run request; collect run artifact directory" as part of the repo build handoff, and this gap needs addressing.
- **Impact**: Unlocks the EVALUATION domain's ability to execute benchmark suites and collect durable, append-only results, which is a prerequisite for the Regression Comparison Engine.

#### 2. File Inventory
- **Create**: `promptops/runtime/runner.py` (The runner shim executable script)
- **Modify**: None
- **Read-Only**:
  - `promptops/schemas/harness-adapter.schema.json`
  - The conceptually described schemas for run requests and run artifacts, which are currently missing.

#### 3. Implementation Spec
- **Runner Architecture**: The runner shim acts as a generic bridge. It reads a run request json file, looks up the specified harness adapter configuration (e.g., `adapter.yaml` in the reference adapter), and invokes the adapter's entrypoint.
- **Manifest Format**: Not applicable.
- **Pseudo-Code**:
  1. Load run request json file.
  2. Parse the specified harness ID.
  3. Load the corresponding harness adapter configuration.
  4. Build the invocation command from the adapter's `entrypoint` and required environment variables defined in the harness adapter schema.
  5. Execute the adapter as a subprocess, passing the run request path.
  6. Wait for the subprocess to complete.
  7. Validate the output directory contains the required run artifact files according to the conceptually described schema.
- **Harness Contract Interface**: Input is a run request json file path. Output is a directory containing artifact components as defined in the conceptually described run artifact schema.
- **Dependencies**:
  - `promptops/schemas/harness-adapter.schema.json`
  - The conceptually described schemas for run requests and run artifacts, which are currently missing.
  - EVALUATION domain tasks depend on this to generate actual run results.

#### 4. Test Plan
- **Verification**: `python promptops/runtime/runner.py`
- **Success Criteria**:
  - `[ $? -ne 0 ]`
- **Edge Cases**:
  - `python promptops/runtime/runner.py --invalid`
  - `[ $? -ne 0 ]`