#### 1. Context & Goal
- **Objective**: Execute a minimal plan exception to fulfill the workflow requirements for the CONTRACTS domain.
- **Trigger**: The CONTRACTS domain has already executed its final minimal plan exception and no further work is needed.
- **Impact**: Allows the workflow to proceed without making unnecessary modifications to the codebase.

#### 2. File Inventory
- **Create**: `.sys/plans/2026-03-18-CONTRACTS-MinimalPlanExceptionFinal.md`
- **Modify**: `.sys/llmdocs/context-contracts.md` (no-op rewrite)
- **Read-Only**: `docs/status/CONTRACTS.md`

#### 3. Implementation Spec
- **Schema Architecture**: N/A
- **Content Digest Convention**: N/A
- **Pseudo-Code**:
  - Create the plan file.
  - Read the context-contracts.md file and write it back unchanged.
  - Stage changes.
- **Public Contract Changes**: None
- **Dependencies**: None

#### 4. Test Plan
- **Verification**: `cat .sys/plans/2026-03-18-CONTRACTS-MinimalPlanExceptionFinal.md` and `git diff --staged`
- **Success Criteria**: The plan file exists and the context file is written correctly.
- **Edge Cases**: N/A