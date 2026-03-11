#### 1. Context & Goal
- **Objective**: Design an automated GitHub Actions workflow to publish immutable GitHub Releases when tags are pushed.
- **Trigger**: The README.md governance primitive for immutable releases and hardened distribution semantics is missing.
- **Impact**: Enforces supply-chain integrity by preventing release assets and tags from being modified after publication, providing an auditable distribution gate.

#### 2. File Inventory
- **Create**: `.github/workflows/immutable-release.yml`
- **Modify**: None.
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
- **Verification**: `mkdir -p test-fixtures/ && echo "v1.0.0" > test-fixtures/tag.txt && tar -czvf promptops.tar.gz promptops/ && [ $? -eq 0 ]`
- **Success Criteria**: `ls promptops.tar.gz && [ $? -eq 0 ]`
- **Edge Cases**: `[ ! -f promptops.tar.gz ] && echo "Build failed"`