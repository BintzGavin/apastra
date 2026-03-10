#### 1. Context & Goal
- **Objective**: Establish the foundational code ownership and review boundaries for the PromptOps repository.
- **Trigger**: The `README.md` requires CODEOWNERS to enforce review boundaries on prompts, policies, harness specs, and delivery targets, but `.github/CODEOWNERS` does not exist.
- **Impact**: Enforces that changes to critical domain assets (prompts, policies, delivery targets, evaluation suites) cannot be merged without explicit approval from designated domain owners, establishing the human checkpoint required by the Black Hole Architecture.

#### 2. File Inventory
- **Create**: `.github/CODEOWNERS` (Defines domain-specific reviewers for critical paths)
- **Modify**: None
- **Read-Only**: `README.md` (for governance primitive requirements)

#### 3. Implementation Spec
- **Policy Architecture**: GitHub's native `CODEOWNERS` feature will be used to automatically request reviews from designated teams or individuals when changes are made to specific directory paths.
- **Workflow Design**: N/A (GitHub native feature)
- **CODEOWNERS Patterns**:
  - `promptops/prompts/` @apastra/prompt-engineers
  - `promptops/policies/` @apastra/governance-admins
  - `promptops/evaluators/` @apastra/evaluation-team
  - `promptops/suites/` @apastra/evaluation-team
  - `promptops/delivery/` @apastra/governance-admins
  - `derived-index/promotions/` @apastra/governance-admins
  - `.github/workflows/` @apastra/infrastructure
- **Dependencies**: No external dependencies. Requires GitHub branch protection rules to "Require review from Code Owners" to be fully effective.

#### 4. Test Plan
- **Verification**: Open a test pull request modifying a file in `promptops/prompts/` and verify that `@apastra/prompt-engineers` is automatically requested for review.
- **Success Criteria**: Review requests are automatically assigned to the correct teams based on the paths modified in a PR.
- **Edge Cases**: Modifying files across multiple domains (e.g., both a prompt and a policy) must correctly request reviews from all relevant code owners.
