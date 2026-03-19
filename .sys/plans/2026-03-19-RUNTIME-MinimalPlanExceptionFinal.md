#### 1. Context & Goal
- **Objective**: Execute a final minimal plan exception for the RUNTIME domain.
- **Trigger**: The runtime architecture resolver chain and consumption manifest implementation is finalized.
- **Impact**: Unlocks final repository state for completion.

#### 2. File Inventory
- **Create**: `.sys/plans/2026-03-19-RUNTIME-MinimalPlanExceptionFinal.md`
- **Modify**: `.sys/llmdocs/context-runtime.md` (no-op write)
- **Read-Only**: `promptops/schemas/`

#### 3. Implementation Spec
- **Resolver Architecture**: No changes.
- **Manifest Format**: No changes.
- **Pseudo-Code**: N/A
- **Harness Contract Interface**: N/A
- **Dependencies**: None.

#### 4. Test Plan
- **Verification**: Ensure the file `.sys/llmdocs/context-runtime.md` is reconstructed exactly byte-for-byte.
- **Success Criteria**: `git diff` shows no unintended modifications to `.sys/llmdocs/context-runtime.md`.
- **Edge Cases**: None.
