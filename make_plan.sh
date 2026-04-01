cat << 'PLAN' > .sys/plans/$(date +%Y-%m-%d)-EVALUATION-StarterPacksGeneration.md
#### 1. Context & Goal
- **Objective**: Implement a script to generate community starter packs.
- **Trigger**: The docs/vision.md requires "Starter packs (5-10 packs)" under Expansion 5 to bootstrap the community registry path, and it is marked as P2.
- **Impact**: Bootstraps the registry path by providing curated starter packs for common workflows (summarization, extraction, classification, code review).

#### 2. File Inventory
- **Create**: `promptops/harnesses/generate-starter-packs.sh` (Bash script to generate starter pack structures)
- **Modify**: N/A
- **Read-Only**: `docs/vision.md` (Expansion 5), `promptops/schemas/community-prompt-pack.schema.json`

#### 3. Implementation Spec
- **Harness Architecture**: A standalone bash script in `promptops/harnesses/` that will generate community starter pack directories. These packs include pre-built datasets, evaluators, suites, and prompt specs. The script creates the basic skeleton for 4 mentioned types: summarization, extraction, classification, and code review.
- **Run Request Format**: N/A
- **Run Artifact Format**: Output directory containing starter packs.
- **Pseudo-Code**:
  - `mkdir -p derived-index/starter-packs/{summarization,extraction,classification,code-review}`
  - Create basic YAML/JSON files matching schemas within each pack.
- **Baseline and Regression Flow**: Starter packs provide initial baselines.
- **Dependencies**: Depends on `community-prompt-pack.schema.json` from CONTRACTS schema.

#### 4. Test Plan
- **Verification**: Run `bash promptops/harnesses/generate-starter-packs.sh` and verify directories are created.
- **Success Criteria**: The directories for the starter packs are created with skeletal files.
- **Edge Cases**: Script can handle existing directories without failing.
PLAN
