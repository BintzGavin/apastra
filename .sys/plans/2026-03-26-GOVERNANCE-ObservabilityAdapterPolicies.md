#### 1. Context & Goal
- **Objective**: Define governance policies for observability adapter delivery targets.
- **Trigger**: `docs/vision.md` outlines "Observability adapter delivery policies" as an expansion governance feature to define rules for how run artifacts are emitted to external observability systems (Langfuse, OpenTelemetry) via delivery adapters, and policies for what data is sent and to whom.
- **Impact**: Establishes clear governance rules for emitting sensitive evaluation data to third-party observability platforms, ensuring auditability and compliance.

#### 2. File Inventory
- **Create**: `promptops/policies/observability-adapters.md` (Defines governance rules for configuring and using observability adapters like Langfuse and OpenTelemetry).
- **Modify**: `.github/CODEOWNERS` (Add the new policy file to the `@apastra/governance-admins` review boundary).
- **Read-Only**: `docs/vision.md` (Observability bridge adapters section).

#### 3. Implementation Spec
- **Policy Architecture**: The policy will mandate that all observability adapters defined in `promptops/delivery/` must explicitly declare which data types (e.g., `scorecard`, `regression_report`, `run_manifest`, `cases`) are permitted to be emitted. It will also require that endpoints must use secure connections (HTTPS/TLS) and that sensitive credentials (like API keys) must be managed via GitHub Secrets or an equivalent secure secret store, not hardcoded in the adapter configurations.
- **Workflow Design**: N/A
- **CODEOWNERS Patterns**: Add `/promptops/policies/observability-adapters.md @apastra/governance-admins` to `.github/CODEOWNERS`
- **Promotion Record Format**: N/A
- **Delivery Target Format**: N/A
- **Dependencies**: N/A

#### 4. Test Plan
- **Verification**: Verify the creation of `promptops/policies/observability-adapters.md` and the update to `.github/CODEOWNERS`.
- **Success Criteria**: The policy file exists and clearly articulates the governance rules for observability adapters, and CODEOWNERS enforcement is in place.
- **Edge Cases**: N/A
