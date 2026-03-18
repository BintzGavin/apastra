#### 1. Context & Goal
- **Objective**: Execute a minimal plan exception to confirm all necessary contracts (schemas, validators, foundational files) are complete and the system vision is satisfied.
- **Trigger**: The CONTRACTS domain has successfully documented all missing requirements, schemas, and instances from `docs/vision.md`, ensuring all other domains have their foundation.
- **Impact**: Unlocks RUNTIME, EVALUATION, and GOVERNANCE by completing the final foundational architecture requirements for prompt-spec, suite, evaluators, dataset-schemas, moderation, and artifact-refs.

#### 2. File Inventory
- **Create**: `.sys/plans/2026-03-18-CONTRACTS-MinimalPlanExceptionFinal-v0.61.0.md`
- **Modify**: `.sys/llmdocs/context-contracts.md` (no-op write), `.jules/CONTRACTS.md`, `docs/progress/CONTRACTS.md`, `docs/status/CONTRACTS.md`
- **Read-Only**: `docs/vision.md`

#### 3. Implementation Spec
- **Schema Architecture**: No new schema architecture changes required.
- **Content Digest Convention**: N/A
- **Pseudo-Code**: N/A
- **Public Contract Changes**: Version bump to `v0.61.0`
- **Dependencies**: None.

#### 4. Test Plan
- **Verification**: `cat .sys/plans/2026-03-18-CONTRACTS-MinimalPlanExceptionFinal-v0.61.0.md` and `cat .sys/llmdocs/context-contracts.md`
- **Success Criteria**: All updates are correctly reflected in the repository and files are written correctly.
- **Edge Cases**: N/A
