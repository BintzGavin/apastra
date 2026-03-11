#### 1. Context & Goal
- **Objective**: Design an automated GitHub Actions workflow to publish immutable GitHub Releases when tags are pushed.
- **Trigger**: The README.md governance primitive for immutable releases and hardened distribution semantics is missing.
- **Impact**: Enforces supply-chain integrity by preventing release assets and tags from being modified after publication, providing an auditable distribution gate.

#### 2. File Inventory
- **Create**:
  - A new GitHub Actions workflow file in `.github/workflows/`
- **Modify**: []
- **Read-Only**: `README.md`

#### 3. Implementation Spec
- **Policy Architecture**: Workflow triggers on tag push (`refs/tags/*`). It packages the prompts, computes the content digest, creates a GitHub Release using the `gh` CLI, and attaches the packages as release assets.
- **Workflow Design**:
  - `on: push: tags: - '*'`
  - `jobs: release:`
    - Checkout code using `actions/checkout`
    - Package prompts using `tar -czvf promptops.tar.gz promptops/`
    - Compute digest using `sha256sum promptops.tar.gz | awk '{print $1}'`
    - Create GitHub Release using `gh release create`
- **CODEOWNERS Patterns**: N/A
- **Promotion Record Format**: N/A
- **Delivery Target Format**: N/A
- **Dependencies**: None.

#### 4. Test Plan
- **Verification**: `echo 'No tests required'`
- **Success Criteria**: `echo 'No tests required'`
- **Edge Cases**: `echo 'No tests required'`
