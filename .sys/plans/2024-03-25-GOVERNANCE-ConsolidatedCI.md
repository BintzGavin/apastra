#### 1. Context & Goal
- **Objective**: Create the simplified two-workflow "Consolidated CI mode" setup for teams upgrading from local-first to CI.
- **Trigger**: `docs/vision.md` outlines a "Consolidated CI mode" containing `prompt-eval.yml` and `prompt-release.yml` for basic CI, which are currently missing from `.github/workflows/`.
- **Impact**: Provides a lower-friction entry point for CI adoption by consolidating regression gating, release immutability, and promotion recording into two simple workflows, as promised by the vision doc.

#### 2. File Inventory
- **Create**:
  - `.github/workflows/prompt-eval.yml` (Basic CI workflow to run regression suites on PRs)
  - `.github/workflows/prompt-release.yml` (Basic CI workflow to create immutable releases and append promotion records on tag push)
- **Modify**: None
- **Read-Only**: `docs/vision.md` ("Consolidated CI mode" section), existing `.github/workflows/regression-gate.yml`, `.github/workflows/immutable-release.yml`, and `.github/workflows/promote.yml` for reference.

#### 3. Implementation Spec
- **Policy Architecture**: Implement the "Consolidated CI mode" approach that combines multiple governance steps into two easy-to-use workflows, serving as a stepping stone to the full six-workflow enterprise setup.
- **Workflow Design**:
  - `prompt-eval.yml`: Triggered on `pull_request` affecting `promptops/**`. It should act as a regression gate by checking the regression report and posting results, blocking the merge if regressions are detected.
  - `prompt-release.yml`: Triggered on `push` with `tags`. It should package prompts, create an immutable GitHub release, and immediately append a promotion record for the release digest.
- **CODEOWNERS Patterns**: No changes needed; workflows are already owned by `@apastra/infrastructure`.
- **Promotion Record Format**: No changes needed; leverages the existing structure.
- **Delivery Target Format**: No changes needed.
- **Dependencies**: The existing regression report format from EVALUATION must be stable to enforce the gate in `prompt-eval.yml`.

#### 4. Test Plan
- **Verification**: `ls -l .github/workflows/prompt-eval.yml .github/workflows/prompt-release.yml`
- **Success Criteria**: Both YAML files exist, are syntactically valid GitHub Actions workflows, and match the descriptions in `docs/vision.md`.
- **Edge Cases**: Missing regression report fails the gate correctly.