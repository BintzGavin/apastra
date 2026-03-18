#### 1. Context & Goal
- **Objective**: Execute a Minimal Plan Exception for the RUNTIME domain.
- **Trigger**: The RUNTIME domain has already executed its final minimal plan exception (status log is at `v1.38.0` with `MinimalPlanExceptionFinal`). All critical vision gaps from `docs/vision.md` and `README.md` regarding the resolver chain, consumption manifests, packaged artifact fetching, and local overrides are complete.
- **Impact**: Unlocks the continuous run of the agent workflow by satisfying the executor's dependency on a new plan spec file without forcing redundant, out-of-scope work.

#### 2. File Inventory
- **Create**: `.sys/plans/2026-03-18-RUNTIME-MinimalPlanExceptionFinal-v1.39.0.md` (this file)
- **Modify**: `.sys/llmdocs/context-runtime.md` (no-op rewrite to fulfill execution requirements)
- **Read-Only**: `docs/vision.md`, `README.md`, `docs/status/RUNTIME.md`

#### 3. Implementation Spec
- **Resolver Architecture**: No changes required.
- **Manifest Format**: No changes required.
- **Pseudo-Code**:
  1. Write the literal bytes of `.sys/llmdocs/context-runtime.md` back to itself.
  2. Verify no-op write with `git diff`.
- **Dependencies**: None.

#### 4. Test Plan
- **Verification**: Run `git diff` to ensure no actual changes were made to the codebase beyond this new spec file.
- **Success Criteria**: The executor can process this file and proceed to completion without modifying any implementation logic.
- **Edge Cases**: None.
