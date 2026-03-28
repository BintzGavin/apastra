#### 1. Context & Goal
- **Objective**: Implement observability bridge adapters for Langfuse and OpenTelemetry.
- **Trigger**: docs/vision.md explicitly defines "Observability bridge adapters" (Expansion 6) to emit run artifacts to existing observability systems like Langfuse and OpenTelemetry, preventing an either/or friction.
- **Impact**: Allows teams to send evaluation outputs directly to their existing observability tools.

#### 2. File Inventory
- **Create**: promptops/runs/emit_observability.py
- **Modify**: None
- **Read-Only**: docs/vision.md

#### 3. Implementation Spec
- **Harness Architecture**: A new Python script emit_observability.py will read the observability configuration (e.g. from promptops/delivery/observability.yaml or a run manifest) and push specified evaluation artifacts (scorecard, regression report, run manifest) to the configured backends (Langfuse API or OTEL endpoint).
- **Run Request Format**: Unchanged.
- **Run Artifact Format**: Unchanged.
- **Pseudo-Code**:
  ```python
  import json, sys, os
  # load observability config
  # load specified artifacts (scorecard.json, run_manifest.json, etc.)
  # for each adapter in config:
  #   if type == 'langfuse':
  #     # push to Langfuse API using endpoint
  #   if type == 'opentelemetry':
  #     # push to OTEL endpoint
  ```
- **Baseline and Regression Flow**: Unchanged.
- **Dependencies**: Requires valid schemas from CONTRACTS.

#### 4. Test Plan
- **Verification**: Run python promptops/runs/emit_observability.py --dry-run to test configuration loading and payload construction without actual network requests.
- **Success Criteria**: The script successfully loads the observability config, reads the selected artifacts, and formats the correct payload for each specified adapter.
- **Edge Cases**: Missing artifacts, unreachable endpoints, invalid configuration.
