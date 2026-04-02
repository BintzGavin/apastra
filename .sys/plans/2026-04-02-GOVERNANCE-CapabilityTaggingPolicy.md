#### 1. Context & Goal
- **Objective**: Implement a capability tagging policy to govern how suite tags map to human oversight and automated promotion gates.
- **Trigger**: The CONTRACTS domain has successfully unblocked this task by adding the `tags` and `tier` fields to the `suite.schema.json`.
- **Impact**: Enforces standardized metadata use in evaluation execution and creates an auditable link between tag declarations and registry promotion rules.

#### 2. File Inventory
- **Create**: [promptops/policies/capability-tagging.md]
- **Modify**: []
- **Read-Only**: []

#### 3. Implementation Spec
- **Policy Architecture**: The policy will define how capability tags defined in `suite.schema.json` are interpreted during the promotion process (e.g., specific tags may require specialized expert reviews, or skip certain automated checks).
- **Workflow Design**: N/A (Policy specification document only).
- **CODEOWNERS Patterns**: Add `promptops/policies/capability-tagging.md` to `.github/CODEOWNERS` under `@promptops-governance`.
- **Promotion Record Format**: N/A
- **Delivery Target Format**: N/A
- **Dependencies**: CONTRACTS `suite.schema.json` (Resolved)

#### 4. Test Plan
- **Verification**: Review `promptops/policies/capability-tagging.md` against `suite.schema.json` to ensure alignment on the use of `tags`. Verify `.github/CODEOWNERS` update.
- **Success Criteria**: The policy document clearly maps capability tags to review and promotion expectations.
- **Edge Cases**: Empty or unregistered tags should fall back to a default, restricted review path.
