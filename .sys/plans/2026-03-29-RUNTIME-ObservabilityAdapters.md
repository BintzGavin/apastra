#### 1. Context & Goal
- **Objective**: Implement observability bridge adapters to emit run artifacts to systems like Langfuse and OpenTelemetry.
- **Trigger**: `docs/vision.md` explicitly calls out "Expansion 6: Observability bridge adapters" to emit metrics and reduce friction for teams already using observability platforms.
- **Impact**: Unlocks integration with existing observability platforms, allowing teams to use the system alongside their current monitoring stacks. Downstream observability tools can receive `scorecard.json`, `run_manifest.json`, etc.

#### 2. File Inventory
- **Create**: `promptops/runtime/observability.py` (Implement observability adapter logic to parse the config and dispatch payloads)
- **Modify**: `promptops/runtime/runner.py` (Call the observability emitting function after artifacts are generated and validated)
- **Read-Only**: `docs/vision.md`, `promptops/schemas/observability-adapter-config.schema.json`

#### 3. Implementation Spec
- **Resolver Architecture**: No change to resolver chain. The observability logic hooks into the runner post-execution.
- **Manifest Format**: Uses `promptops/schemas/observability-adapter-config.schema.json` loaded from `promptops/delivery/observability.yaml`.
- **Pseudo-Code**:
  In `observability.py`:
  ```python
  def emit_artifacts(output_dir):
      # Load promptops/delivery/observability.yaml
      # Validate against schema
      # For each adapter configured:
      #   Read requested emit files (e.g. scorecard.json) from output_dir
      #   If type == 'langfuse':
      #       # emit to Langfuse endpoint
      #   elif type == 'opentelemetry':
      #       # emit to OpenTelemetry endpoint
      #   # For this version, mock HTTP requests/prints if external deps are missing
  ```
  In `runner.py`:
  ```python
  # After validation is successful:
  from promptops.runtime.observability import emit_artifacts
  try:
      emit_artifacts(output_dir)
  except Exception as e:
      print(f"Warning: Failed to emit observability artifacts: {e}")
  ```
- **Harness Contract Interface**: No changes to the core interface.
- **Dependencies**: Depends on the existing `promptops/schemas/observability-adapter-config.schema.json`.

#### 4. Test Plan
- **Verification**: Run `python promptops/runtime/runner.py <request> <adapter> <output_dir>` with a mock `promptops/delivery/observability.yaml` configured. Check the stdout/logs to verify the adapter correctly attempted to emit the specified artifacts.
- **Success Criteria**: The observability integration attempts to emit the appropriate files for each configured adapter type without failing the core runner execution.
- **Edge Cases**: Missing config file, invalid schema, missing requested emit file, network failure during emit.
