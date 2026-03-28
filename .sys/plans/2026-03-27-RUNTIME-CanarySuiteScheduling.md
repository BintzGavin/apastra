#### 1. Context & Goal
- **Objective**: Implement runtime support for scheduling and executing canary suites to detect post-ship quality erosion.
- **Trigger**: The "drift detection" capability in docs/vision.md, requiring canary suites to run on a schedule and emit drift reports.
- **Impact**: Enables detection of model provider silent updates and output drift, protecting production quality post-shipment.

#### 2. File Inventory
- **Create**:
  - `promptops/runtime/canary.py` - Logic to manage scheduling, execution, and alerting for canary suites.
- **Modify**:
  - `promptops/runtime/cli.py` - Add a `canary` command to trigger or schedule canary suites.
  - `promptops/runtime/resolve.py` - Update metadata generation to include baseline references needed for drift comparisons.
- **Read-Only**:
  - `promptops/schemas/suite.schema.json` - To understand suite and scorecard references.
  - `docs/vision.md` - Canary and drift detection requirements.

#### 3. Implementation Spec
- **Resolver Architecture**: No changes to the core resolution sequence. Canary execution will fetch the referenced suite via the existing resolution chain.
- **Manifest Format**: Canary definitions will exist in `promptops/canaries/` (or similarly defined path per vision) specifying `schedule`, `suite_ref`, and `alert` blocks. The runtime will parse these files.
- **Pseudo-Code**:
  - CLI command `promptops.runtime.cli canary run <canary_id>` loads the canary spec.
  - It calls `runner.py` to execute the referenced suite.
  - It compares the resulting scorecard against the production baseline (similar to regression checking).
  - If drift is detected (thresholds violated), it triggers the configured alert mechanism (e.g., stdout for now, structured for integrations).
- **Harness Contract Interface**: Relies on the existing `run request in -> run artifact out` contract.
- **Dependencies**: Requires `suite.schema.json` and scorecard formats defined by CONTRACTS.

#### 4. Test Plan
- **Verification**: Run `python -m promptops.runtime.cli canary run test-canary` with a mocked canary spec that predictably fails a drift check.
- **Success Criteria**: The command should output a drift report indicating failure and the specific metrics that drifted.
- **Edge Cases**: Missing suite reference, no baseline available, invalid schedule format, suite passes but drift is within acceptable limits.
