#### 1. Context & Goal
- **Objective**: Implement a governance policy defining tiered evaluation suites (smoke, regression, capability) and mandatory release-candidate gates.
- **Trigger**: The docs/vision.md document explicitly lists "Tiered suites + capability tagging + forcing release-candidate gates" as the required mitigation for the "False confidence" risk (narrow suites missing real failures).
- **Impact**: Establishes formal tiering requirements for prompt evaluation and enforces that production promotions are gated by a comprehensive release-candidate suite, preventing regressions caused by overfitting to narrow test sets.

#### 2. File Inventory
- **Create**: promptops/policies/tiered-suites.md (Defines the suite tiering hierarchy, required test mix, and gating rules for promotions)
- **Modify**: None
- **Read-Only**: docs/vision.md (Risks and mitigations section), promptops/schemas/suite.schema.json, promptops/schemas/promotion-record.schema.json

#### 3. Implementation Spec
- **Policy Architecture**: The policy will define three formal tiers: Smoke (fast iteration, local only), Regression (PR gating, core capabilities), and Release-Candidate (exhaustive, capability-based, promotion gating).
- **Workflow Design**:
  - CI/CD pipelines must enforce that `regression-gate.yml` requires at least the "Regression" tier to pass.
  - `promote.yml` and `immutable-release.yml` must enforce that the baseline passed the "Release-Candidate" tier before appending a promotion record.
- **CODEOWNERS Patterns**: No changes; governed by existing `@apastra/governance-admins` rules for `promptops/policies/`.
- **Promotion Record Format**: No structural changes to the schema, but the policy mandates that the referenced `evidence.run_id` in the promotion record must originate from a Release-Candidate suite execution.
- **Delivery Target Format**: N/A
- **Dependencies**: Depends on EVALUATION domain extending the `suite.schema.json` to include a `tier` or `tags` array to label suites as `release-candidate` or `regression`.

#### 4. Test Plan
- **Verification**: Review the newly created `promptops/policies/tiered-suites.md` against the vision requirements for mitigating "False confidence".
- **Success Criteria**: The policy clearly defines the suite tiers, their execution context (local vs. PR vs. release), and explicitly mandates a release-candidate gate for promotions.
- **Edge Cases**: Defines handling for emergency hotfixes where a full release-candidate suite execution might be bypassed via documented exceptions.
