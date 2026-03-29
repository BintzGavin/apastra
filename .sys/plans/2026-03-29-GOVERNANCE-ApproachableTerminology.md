#### 1. Context & Goal
- **Objective**: Establish governance policy for approachable terminology, specifically regarding the term "harness".
- **Trigger**: docs/vision.md "Refinement 5: Approachable terminology" specifies that user-facing documentation should refer to "your agent" everywhere and reserve "harness" for the technical specification.
- **Impact**: Creates an auditable policy that enforces consistent and approachable terminology across all user-facing documentation and repositories.

#### 2. File Inventory
- **Create**: `promptops/policies/approachable-terminology.md`
- **Modify**: None (Executor handles status updates).
- **Read-Only**: `docs/vision.md` (for refinement reference).

#### 3. Implementation Spec
- **Policy Architecture**: The `approachable-terminology.md` policy must explicitly define the allowed contexts for the terms "agent" and "harness".
- **Workflow Design**: The policy should mandate that documentation PRs are reviewed for terminology consistency.
- **CODEOWNERS Patterns**: The policy file must be owned by `@apastra/governance-admins` to prevent unauthorized changes to the terminology thresholds.
- **Dependencies**: Depends on the DOCS domain to implement the terminology changes.

#### 4. Test Plan
- **Verification**: Review the created `approachable-terminology.md` policy to ensure it clearly defines the boundaries of terminology.
- **Success Criteria**: The policy document explicitly requires that "harness" is reserved for technical specifications and "agent" is used in user-facing contexts.
- **Edge Cases**: What happens if a technical specification is also user-facing? The policy must clarify that the intended audience (developer vs. end-user) determines the appropriate terminology.
