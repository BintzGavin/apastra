#### 1. Context & Goal
- **Objective**: Define GitHub Rulesets to enforce branch protections and tag immutability.
- **Trigger**: README.md requires branch protections and rulesets to ensure checks pass before merging to protected branches, and tags remain immutable.
- **Impact**: Enforces that the `Regression Gate` check must pass before merging to `main`, and protects tags from being mutated or deleted.

#### 2. File Inventory
- **Create**: Conceptual rulesets for main branch protection and tag immutability.
- **Modify**: None.
- **Read-Only**: `README.md` (Rulesets section), `.github/workflows/regression-gate.yml` (status check name).

#### 3. Implementation Spec
- **Policy Architecture**: GitHub rulesets natively configure repository protections. The main branch ruleset will target the default branch, enforcing required pull request reviews and status checks (specifically the `gate` job from `Regression Gate`). The tag ruleset will target all tags (`refs/tags/*`), enforcing that tags can only be created, not updated or deleted.
- **Workflow Design**: These are declarative GitHub configurations, not workflows.
- **CODEOWNERS Patterns**: No changes.
- **Promotion Record Format**: No changes.
- **Delivery Target Format**: No changes.
- **Dependencies**: `Regression Gate` workflow must exist and run a job named `gate`.

#### 4. Test Plan
- **Verification**: `echo 'No tests required'`
- **Success Criteria**: `echo 'No tests required'`
- **Edge Cases**: `echo 'No edge cases tested'`