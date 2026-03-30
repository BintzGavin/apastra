#### 1. Context & Goal
- **Objective**: Implement a governance policy for dataset holdout sets to prevent overfitting.
- **Trigger**: `docs/vision.md` outlines "Maintain holdout sets for release candidates" and lists holdouts as the primary mitigation for benchmark gaming.
- **Impact**: Establishes formal governance expectations around dataset holdouts for pre-release validation, ensuring teams cannot over-optimize for narrow benchmarks.

#### 2. File Inventory
- **Create**: `promptops/policies/holdout-sets.md` (Formal policy document outlining the use and requirement of holdout datasets for release candidate suites)
- **Modify**: N/A
- **Read-Only**: `docs/vision.md` (Prevent overfitting section, Risks and mitigations table)

#### 3. Implementation Spec
- **Policy Architecture**:
  - Define rules for what constitutes a valid holdout set.
  - Mandate that holdout sets must be used for all suites designated as release candidates.
  - Specify that holdout datasets should be excluded from routine developer iteration to maintain their integrity.
  - Require that the regression policy engine and promotion records evaluate release candidates against these holdout sets.
- **Workflow Design**: N/A (Policy document only)
- **CODEOWNERS Patterns**: Handled by existing `promptops/policies/` mapping to `@apastra/governance-admins`.
- **Promotion Record Format**: The promotion record should reflect passing results specifically against the designated holdout sets for release candidates.
- **Delivery Target Format**: N/A
- **Dependencies**: CONTRACTS (dataset schemas to support holdout tagging, suite schemas).

#### 4. Test Plan
- **Verification**: Verify that `promptops/policies/holdout-sets.md` is created and accurately reflects the requirements outlined in `docs/vision.md` for holdout sets.
- **Success Criteria**: The holdout sets policy document is present in `promptops/policies/` and clearly defines the usage and requirement of holdouts for release candidates.
- **Edge Cases**: Ensure the policy accounts for edge cases where holdout sets need to be rotated or updated without compromising the integrity of past benchmarks.
