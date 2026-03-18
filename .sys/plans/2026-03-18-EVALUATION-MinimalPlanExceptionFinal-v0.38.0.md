#### 1. Context & Goal
- **Objective**: Create a minimal exception plan.
- **Trigger**: The Minimal Plan Exception Final is required.
- **Impact**: Unlocks the final state of the Minimal Plan Exception.

#### 2. File Inventory
- **Create**: `.sys/plans/2026-03-18-EVALUATION-MinimalPlanExceptionFinal-v0.38.0.md` (A blank file or minimal file)
- **Modify**: `.sys/llmdocs/context-evaluation.md` (no-op write)
- **Read-Only**: none

#### 3. Implementation Spec
- **Harness Architecture**: N/A
- **Run Request Format**: N/A
- **Run Artifact Format**: N/A
- **Pseudo-Code**:
  1. Create plan file.
  2. No-op write to `.sys/llmdocs/context-evaluation.md`.
- **Baseline and Regression Flow**: N/A
- **Dependencies**: N/A

#### 4. Test Plan
- **Verification**: Ensure the files are created and unmodified respectively.
- **Success Criteria**: `ls -la .sys/plans/` shows the new file, `git diff` shows no changes for the context file.
- **Edge Cases**: N/A