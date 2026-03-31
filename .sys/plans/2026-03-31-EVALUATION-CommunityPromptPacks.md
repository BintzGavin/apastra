#### 1. Context & Goal
- **Objective**: Spec the execution flow to run starter pack suites and generate their pre-built baselines.
- **Trigger**: The vision document (Expansion 5) describes community prompt packs (starter packs like summarization, extraction) to bootstrap the registry, which require pre-built baselines.
- **Impact**: Automates the creation of ready-to-use evaluation baselines for community packs.

#### 2. File Inventory
- **Create**: `promptops/harnesses/generate_community_baselines.sh`
- **Modify**: None
- **Read-Only**: `promptops/schemas/community-prompt-pack.schema.json`, `docs/vision.md`

#### 3. Implementation Spec
- **Harness Architecture**: Leverage the reference adapter to invoke each suite defined in the community prompt pack.
- **Run Request Format**: Use existing run request logic referencing the pack's suite ID.
- **Run Artifact Format**: Standard scorecard output which becomes the baseline.
- **Pseudo-Code**:
  - Read `community-prompt-pack.json`.
  - Iterate through declared `suites`.
  - Construct a run request for each suite.
  - Execute via harness reference adapter.
  - Store the output scorecard as a baseline in `derived-index/baselines/`.
- **Baseline and Regression Flow**: Populates the baselines directory so downstream regression gating is immediately functional for starter pack consumers.
- **Dependencies**: CONTRACTS `community-prompt-pack.schema.json`, RUNTIME pack resolver.

#### 4. Test Plan
- **Verification**: Run `wc -l .sys/plans/2026-03-31-EVALUATION-CommunityPromptPacks.md`
- **Success Criteria**: The spec file exists and matches the required EVALUATION template.
- **Edge Cases**: Empty suites list, missing suite files.
