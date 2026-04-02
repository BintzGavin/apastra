#### 1. Context & Goal
- **Objective**: Implement an evidence cases policy to prevent benchmark gaming.
- **Trigger**: The docs/vision.md explicitly requires "require evidence cases" as a mitigation for "Benchmark gaming" where teams optimize for a benchmark score.
- **Impact**: Establishes a governance requirement that evaluation suites and pull requests must include explicit evidence cases (e.g. traced dataset inputs/outputs) to prove claims, preventing optimization of aggregate scores without qualitative proof.

#### 2. File Inventory
- **Create**: promptops/policies/evidence-cases.md
- **Modify**: []
- **Read-Only**: [docs/vision.md]

#### 3. Implementation Spec
- **Policy Architecture**: Define what constitutes an "evidence case" (e.g. a dataset case with explicit assertions or qualitative output that proves a specific capability) and require their inclusion in suites or PRs to validate benchmark scores.
- **Workflow Design**: N/A
- **CODEOWNERS Patterns**: N/A
- **Promotion Record Format**: N/A
- **Delivery Target Format**: N/A
- **Dependencies**: None.

#### 4. Test Plan
- **Verification**: Ensure promptops/policies/evidence-cases.md is created and accurately reflects the "require evidence cases" requirement from docs/vision.md.
- **Success Criteria**: The policy file exists and establishes the governance rule for requiring evidence cases.
- **Edge Cases**: Edge cases around subjective evidence or incomplete logs should be addressed by requiring structured assertions or raw artifact links.
