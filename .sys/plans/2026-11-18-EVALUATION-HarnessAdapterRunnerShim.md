#### 1. Context & Goal
- **Objective**: Implement a runner shim script that invokes a harness adapter and collects its run artifact directory.
- **Trigger**: The docs/vision.md Appendix E explicitly calls out "Implement runner shim: invoke harness adapter with run request; collect run artifact directory" as a required phase.
- **Impact**: Unlocks the ability to execute evaluations via configured harness adapters in a standardized way.

#### 2. File Inventory
- **Create**: `promptops/runs/runner-shim.sh`
- **Modify**: None
- **Read-Only**: `docs/vision.md`, `promptops/schemas/harness-adapter.schema.json`

#### 3. Implementation Spec
- **Harness Architecture**: The runner shim reads the `adapter.yaml` (validating against `harness-adapter.schema.json`), extracts the `entrypoint`, and executes it by passing the run request and an output directory. It then returns the path to the collected artifacts.
- **Run Request Format**: Takes the path to a `run_request.json` file.
- **Run Artifact Format**: Expects the harness to output artifacts into the specified directory (`run_manifest.json`, `scorecard.json`, etc.).
- **Pseudo-Code**:
  ```bash
  # promptops/runs/runner-shim.sh
  # Usage: ./runner-shim.sh <adapter_yaml> <run_request> <output_dir>
  # 1. Parse 'entrypoint' from <adapter_yaml> using yq
  # 2. Execute: $entrypoint <run_request> <output_dir>
  # 3. Verify output artifacts exist in <output_dir>
  ```
- **Baseline and Regression Flow**: N/A
- **Dependencies**: CONTRACTS `harness-adapter.schema.json`, RUNTIME resolver availability

#### 4. Test Plan
- **Verification**: Run `promptops/runs/runner-shim.sh promptops/harnesses/reference-adapter/adapter.yaml test_req.json output_test`
- **Success Criteria**: The script successfully executes the `entrypoint` defined in the adapter YAML, outputting valid artifacts in `output_test`.
- **Edge Cases**: Adapter YAML missing, entrypoint command fails, output directory permissions, run request invalid.
