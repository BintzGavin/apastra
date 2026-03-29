#### 1. Context & Goal
- **Objective**: Establish a governance policy that defines acceptable limits for "prompt debt" and rules for gating code changes based on Audit skill severity scores.
- **Trigger**: The `docs/vision.md` (Expansion 1: Audit skill) introduces a system that scans codebases for hardcoded, untested prompts and reports a severity score ("prompt debt").
- **Impact**: Enforces quality by ensuring that excessive unversioned and untested prompts trigger governance gates, preventing the unchecked accumulation of prompt debt.

#### 2. File Inventory
- **Create**: `promptops/policies/prompt-debt.md` (Governance rules defining acceptable prompt debt limits, gating thresholds, and remediation requirements)
- **Modify**: `.sys/llmdocs/context-governance.md` (Add the new policy to the inventory)
- **Read-Only**: `docs/vision.md` (Expansion 1: Audit skill)

#### 3. Implementation Spec
- **Policy Architecture**: The policy file defines the maximum acceptable "prompt debt" severity score. It dictates that any PR increasing the prompt debt severity score beyond the threshold must be blocked by a required status check.
- **Workflow Design**: A PR workflow (pseudo-code) will run the Audit skill, parse the severity score, and fail the check if the debt limit is exceeded or if new debt is introduced without corresponding mitigation.
- **CODEOWNERS Patterns**: Inherits the existing `@apastra/governance-admins` ownership for `promptops/policies/`.
- **Dependencies**: Depends on the EVALUATION/RUNTIME domains to finalize the Audit skill implementation and its severity score output format.

#### 4. Test Plan
- **Verification**: Review the generated policy document to ensure it clearly articulates the gating rules for prompt debt.
- **Success Criteria**: The `promptops/policies/prompt-debt.md` file exists and provides clear governance rules.
- **Edge Cases**: Handles scenarios where legacy repositories have a high initial prompt debt score by defining a "baseline debt" and gating strictly on new debt increases.
