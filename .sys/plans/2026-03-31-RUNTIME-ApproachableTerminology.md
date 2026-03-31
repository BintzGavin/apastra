#### 1. Context & Goal
- **Objective**: Identify that the required changes for "Approachable terminology" are minimal to none within the RUNTIME executor paths, resulting in a Minimal Plan Exception.
- **Trigger**: "Refinement 5: Approachable terminology" in docs/vision.md.
- **Impact**: Progresses the RUNTIME domain tracking by acknowledging that user-facing CLI and log strings in current Python scripts do not heavily use the "harness" terminology in a way that needs adjustment, or it has been decided that existing CLI args and logic already use "adapter" correctly, aligning with the agent-as-harness paradigm.

#### 2. File Inventory
- **Create**: None
- **Modify**: None
- **Read-Only**: `promptops/runtime/cli.py`, `promptops/runtime/runner.py`, `promptops/runtime/resolve.py`

#### 3. Implementation Spec
- **Resolver Architecture**: Minimal Plan Exception.
- **Manifest Format**: Minimal Plan Exception.
- **Pseudo-Code**: Minimal Plan Exception. No code changes required as "harness" is absent from user-facing logs in the targeted files, and is correctly reserved as a technical parameter (`harness_version`) in `resolve.py`.
- **Harness Contract Interface**: Minimal Plan Exception.
- **Dependencies**: None.

#### 4. Test Plan
- **Verification**: Run `grep -in harness promptops/runtime/*.py`
- **Success Criteria**: None.
- **Edge Cases**: None.
