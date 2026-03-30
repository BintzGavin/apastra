#### 1. Context & Goal
- **Objective**: Establish the governance policy for the "Quick eval mode" to ensure it remains a rapid iteration tool and does not become a permanent replacement for structured suites.
- **Trigger**: `docs/vision.md` explicitly defines a "Quick eval format" for rapid iteration that combines prompt, cases, and assertions into a single file, but there is no governance policy enforcing its intended scope and graduation limits.
- **Impact**: Enforces limits on the complexity and permanence of quick evals, creating an auditable boundary that requires teams to graduate to the full protocol structure as complexity grows.

#### 2. File Inventory
- **Create**: `promptops/policies/quick-eval.md` (Defines the scope, limitations, and graduation rules for quick eval files)
- **Modify**: `docs/status/GOVERNANCE.md` (Increment version and append Quick Eval policy completion entry)
- **Read-Only**: `docs/vision.md` (Quick eval mode section), relevant CONTRACTS schemas

#### 3. Implementation Spec
- **Policy Architecture**: The policy will mandate that quick eval files (`promptops/evals/*.yaml`) are explicitly limited to a maximum number of assertions or test cases before they must be refactored into full `prompt-spec`, `dataset`, `evaluator`, and `suite` files. It will also specify that quick evals are for smoke testing and rapid iteration, prohibiting their use as formal release candidates.
- **Workflow Design**: No new workflows are strictly required, but existing validation workflows should ensure that quick eval files validate against the relevant CONTRACTS schemas.
- **CODEOWNERS Patterns**: No changes.
- **Promotion Record Format**: No changes.
- **Delivery Target Format**: No changes.
- **Dependencies**: The relevant CONTRACTS schemas must be present and correctly defined.

#### 4. Test Plan
- **Verification**: Verify the newly created policy file exists at `promptops/policies/quick-eval.md` and contains the correct graduation requirements.
- **Success Criteria**: The policy accurately reflects the "Quick eval mode" documentation from `docs/vision.md` and establishes clear governance boundaries.
- **Edge Cases**: N/A - The document serves as policy guidance rather than executable logic.
