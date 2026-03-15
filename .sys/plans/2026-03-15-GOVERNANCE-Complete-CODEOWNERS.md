#### 1. Context & Goal
- **Objective**: Update `.github/CODEOWNERS` to cover missing domain paths.
- **Trigger**: The vision document lists harness specs and delivery targets as critical paths for CODEOWNERS, and `promptops/harnesses/`, `promptops/runs/`, `derived-index/baselines/`, and `derived-index/regressions/` (owned by EVALUATION), and `promptops/manifests/`, `promptops/resolver/`, `promptops/runtime/` (owned by RUNTIME), and `promptops/datasets/`, `promptops/evals/`, `promptops/validators/` (owned by CONTRACTS) need owners defined to match the architecture.
- **Impact**: Enforces review boundaries for all domain paths, ensuring changes to runtime, evaluation, and contracts files are reviewed by the correct teams.

#### 2. File Inventory
- **Create**: None
- **Modify**: `.github/CODEOWNERS`
- **Read-Only**: `docs/vision.md`, `README.md`, `.sys/llmdocs/context-governance.md`

#### 3. Implementation Spec
- **Policy Architecture**: The CODEOWNERS file enforces review boundaries by mapping paths to GitHub teams.
- **Workflow Design**: N/A
- **CODEOWNERS Patterns**:
  - `promptops/datasets/` @<contracts-team>
  - `promptops/evals/` @<contracts-team>
  - `promptops/validators/` @<contracts-team>
  - `promptops/harnesses/` @<evaluation-team>
  - `promptops/runs/` @<evaluation-team>
  - `derived-index/baselines/` @<evaluation-team>
  - `derived-index/regressions/` @<evaluation-team>
  - `promptops/manifests/` @<runtime-team>
  - `promptops/resolver/` @<runtime-team>
  - `promptops/runtime/` @<runtime-team>
- **Promotion Record Format**: N/A
- **Delivery Target Format**: N/A
- **Dependencies**: N/A

#### 4. Test Plan
- **Verification**: `cat .github/CODEOWNERS`
- **Success Criteria**: The `.github/CODEOWNERS` file contains all specified mappings.
- **Edge Cases**: N/A
