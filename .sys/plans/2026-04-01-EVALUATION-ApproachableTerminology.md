#### 1. Context & Goal
- **Objective**: Identify that the required changes for "Approachable terminology" are minimal to none within the EVALUATION executor paths, resulting in a Minimal Plan Exception.
- **Trigger**: "Refinement 5: Approachable terminology" in docs/vision.md.
- **Impact**: Progresses the EVALUATION domain tracking by acknowledging that user-facing CLI and log strings in current scripts do not heavily use the "harness" terminology in a way that needs adjustment, or it has been decided that existing CLI args and logic already use "adapter" correctly, aligning with the agent-as-harness paradigm.

#### 2. File Inventory
- **Create**: None
- **Modify**: None
- **Read-Only**: `promptops/harnesses/reference-adapter/run.py`

#### 3. Implementation Spec
- **Harness Architecture**: Minimal Plan Exception.
- **Run Request Format**: Minimal Plan Exception.
- **Run Artifact Format**: Minimal Plan Exception. No code changes required as "harness" is absent from user-facing logs in the targeted files, and is correctly reserved as a technical parameter (`harness_version`).
- **Pseudo-Code**: Minimal Plan Exception.
- **Baseline and Regression Flow**: Minimal Plan Exception.
- **Dependencies**: None.

#### 4. Test Plan
- **Verification**: Run `grep -in harness promptops/harnesses/reference-adapter/run.py`
- **Success Criteria**: None.
- **Edge Cases**: None.
