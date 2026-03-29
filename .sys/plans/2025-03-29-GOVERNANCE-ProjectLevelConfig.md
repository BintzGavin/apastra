#### 1. Context & Goal
- **Objective**: Establish governance for project-level configurations and a simplified minimal file structure.
- **Trigger**: The docs/vision.md requires a "Project-level config + simplified minimal mode" to reduce onboarding friction by 50%.
- **Impact**: Defines the policy governing global project settings (like default models, thresholds) and the conditions for minimal mode auto-activation, ensuring consistent evaluation behavior and directory structure governance.

#### 2. File Inventory
- **Create**: `promptops/policies/project-level-config.md` (Defines governance rules for `promptops.config.yaml` and minimal mode structure)
- **Modify**: None
- **Read-Only**: `docs/vision.md` (Project-level config and minimal mode specification)

#### 3. Implementation Spec
- **Policy Architecture**: The policy will state that if a `promptops.config.yaml` exists, its defined defaults (e.g., model, temperature, base thresholds) act as the global baseline for all suites unless explicitly overridden. It will also define the "minimal mode" structure (only `prompts/`, `evals/`, and `baselines/` exist) and govern its auto-activation for repositories with ≤3 prompt specs.
- **Workflow Design**: The GitHub Actions CI/regression gate must read `promptops.config.yaml` (if present) to enforce the globally defined thresholds when a suite omits them.
- **CODEOWNERS Patterns**: `promptops.config.yaml` should be reviewed by `@apastra/governance-admins` to prevent unauthorized weakening of global thresholds.
- **Promotion Record Format**: N/A
- **Delivery Target Format**: N/A
- **Dependencies**: CONTRACTS must support the `promptops.config.yaml` schema.

#### 4. Test Plan
- **Verification**: Review the newly created policy document to ensure it clearly articulates the rules for `promptops.config.yaml` and the minimal file structure.
- **Success Criteria**: The policy file `promptops/policies/project-level-config.md` exists and covers both the global configuration inheritance and minimal mode directory constraints.
- **Edge Cases**: Repositories that exceed the 3 prompt spec limit must be explicitly guided to graduate from minimal mode to the full directory structure.
