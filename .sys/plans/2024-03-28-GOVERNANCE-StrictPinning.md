#### 1. Context & Goal
- **Objective**: Ensure all GitHub Actions in all GOVERNANCE workflows are strictly pinned to specific 40-character commit SHAs instead of floating tags.
- **Trigger**: "GitHub primitives", "Supply-chain tampering" requirement from `docs/vision.md`.
- **Impact**: Enhances supply chain security and ensures reproducible, immutable builds by preventing unexpected changes or malicious code injection from upstream action updates.

#### 2. File Inventory
- **Create**: N/A
- **Modify**:
  - `.github/workflows/auto-merge.yml` (Pin `actions/checkout` to SHA)
  - `.github/workflows/deliver.yml` (Pin `actions/checkout` to SHA)
  - `.github/workflows/moderation-scan.yml` (Pin `actions/checkout` to SHA)
  - `.github/workflows/promote.yml` (Pin `actions/checkout` to SHA)
  - `.github/workflows/record-approval.yml` (Pin `actions/checkout` to SHA)
  - `.github/workflows/regression-gate.yml` (Pin `actions/checkout` and `tj-actions/changed-files` to SHAs)
  - `.github/workflows/secret-scan.yml` (Pin `actions/checkout` to SHA)
- **Read-Only**: `.github/workflows/immutable-release.yml` (Already pinned)

#### 3. Implementation Spec
- **Policy Architecture**: Replace all instances of `uses: actions/checkout@v4` in the governance domain workflows with `uses: actions/checkout@34e114876b0b11c390a56381ad16ebd13914f8d5` (the 40-character SHA for `v4`). Replace all instances of `uses: tj-actions/changed-files@v44` with `uses: tj-actions/changed-files@2d756ea4c53f7f6b397767d8723b3a10a9f35bf2` (the 40-character SHA for `v44`).
- **Workflow Design**: The CI system remains unchanged functionally; this purely hardens the pipeline.
- **CODEOWNERS Patterns**: N/A
- **Promotion Record Format**: N/A
- **Delivery Target Format**: N/A
- **Dependencies**: N/A

#### 4. Test Plan
- **Verification**: Run `grep -r "uses: .*@" .github/workflows/` and ensure all tags use full 40-character SHAs, and no floating `@v` tags remain.
- **Success Criteria**: All GitHub Action workflow invocations are correctly pinned.
- **Edge Cases**: N/A
