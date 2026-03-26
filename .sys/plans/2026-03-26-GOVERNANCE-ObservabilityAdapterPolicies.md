#### 1. Context & Goal
- **Objective**: Implement a formal governance policy for observability adapters, aligning with the "Expansion 6: Observability bridge adapters" from docs/vision.md.
- **Trigger**: The vision document explicitly lists "Observability bridge adapters" and "Observability adapters" as a planned expansion to bridge the gap with existing observability systems like Langfuse and OpenTelemetry.
- **Impact**: Provides clear governance on how observability adapters should securely emit run artifacts and manage credentials within the promptops ecosystem.

#### 2. File Inventory
- **Create**: `promptops/policies/observability-adapters.md`
- **Modify**: `.sys/llmdocs/context-governance.md`
- **Read-Only**: `docs/vision.md`, `README.md`

#### 3. Implementation Spec
- **Policy Architecture**:
  - Create a new markdown policy document defining the rules for observability adapters.
  - Require adapters to be explicitly defined in `promptops/delivery/observability.yaml`.
  - Mandate that adapters must never hardcode credentials and must only use environment variables injected securely by the runner.
  - Require adapters to gracefully handle network failures without crashing the core run or evaluation processes.
- **Workflow Design**: No new automated workflows needed, this is a policy document.
- **CODEOWNERS Patterns**: Assign `@apastra/governance-admins` as owners of `promptops/policies/observability-adapters.md` (already covered by glob pattern).
- **Promotion Record Format**: N/A
- **Delivery Target Format**: Mention `promptops/delivery/observability.yaml` as the configuration target.
- **Dependencies**: None.

#### 4. Test Plan
- **Verification**:
  - Ensure the new policy file is valid markdown.
  - Ensure it conforms to the general style of other policies in `promptops/policies/`.
