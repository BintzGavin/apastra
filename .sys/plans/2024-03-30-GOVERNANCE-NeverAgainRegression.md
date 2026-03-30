#### 1. Context & Goal
- **Objective**: Define the governance policy for promoting production incidents into a mandatory "never again" regression suite.
- **Trigger**: `docs/vision.md` specifically requires the system to "Promote regressions from production incidents into a 'never again' regression suite" to prevent overfitting and recurring failures.
- **Impact**: Establishes a formal governance rule for post-incident learning, ensuring that edge cases that caused production failures are captured as test cases and explicitly prevented from recurring in future promotions.

#### 2. File Inventory
- **Create**: `promptops/policies/never-again-regression.md`
- **Modify**: None
- **Read-Only**: `docs/vision.md`

#### 3. Implementation Spec
- **Policy Architecture**:
  - The policy must mandate that any production incident resulting from a prompt failure requires at least one new test case added to a designated `never-again` dataset.
  - The `never-again` dataset must be included in a mandatory suite (e.g., `never-again-suite`) that runs on every PR and promotion.
  - The policy must define a strict 1.0 (100%) pass rate threshold for the `never-again-suite` in the regression policy configuration. No regressions or flakiness are permitted for these historical incident cases.
- **Workflow Design**: Outline the steps an engineer must take after a production incident (identify failure, write minimal reproducible dataset case, assert correct behavior, add to `never-again` dataset).
- **CODEOWNERS Patterns**: No new CODEOWNERS patterns; `promptops/policies/` is already owned by `@apastra/governance-admins`.
- **Promotion Record Format**: N/A
- **Delivery Target Format**: N/A
- **Dependencies**: Relies on the existing EVALUATION suite execution and CONTRACTS schemas for datasets and policies.

#### 4. Test Plan
- **Verification**: Verify that `promptops/policies/never-again-regression.md` is created and correctly details the mandatory inclusion of incident cases, the 100% pass rate requirement, and the incident response workflow.
- **Success Criteria**: The policy document exists and provides clear, actionable instructions for teams to prevent incident recurrence.
- **Edge Cases**: Defines what happens if an incident cannot be reliably reproduced (e.g., due to model provider non-determinism) and how to handle quarantine for these specific cases.
