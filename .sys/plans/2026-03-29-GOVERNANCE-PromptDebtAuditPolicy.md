#### 1. Context & Goal
- **Objective**: Establish governance policy for prompt debt acceptable limits and remediation based on the new audit skill.
- **Trigger**: docs/vision.md "Expansion 1: Audit skill" describes a severity score ("prompt debt") for hardcoded, untested prompts.
- **Impact**: Creates an auditable policy that prevents the introduction of new unversioned prompts and enforces the migration of existing hardcoded prompts to versioned, evaluated assets.

#### 2. File Inventory
- **Create**: `promptops/policies/prompt-debt-governance.md`
- **Modify**: None (Executor handles status updates).
- **Read-Only**: `docs/vision.md` (for expansion reference), `promptops/policies/regression.yaml` (for existing blocking semantics).

#### 3. Implementation Spec
- **Policy Architecture**: The `prompt-debt-governance.md` policy must define "prompt debt" as any prompt string or template not tracked within the `promptops/prompts/` directory.
- **Workflow Design**: The policy should mandate that the `apastra-audit` skill output is evaluated during CI. If the PR introduces *new* prompt debt, it must be a blocking failure. If it reduces prompt debt, it is a pass.
- **CODEOWNERS Patterns**: The policy file must be owned by `@apastra/governance-admins` to prevent unauthorized changes to the acceptable debt thresholds.
- **Dependencies**: Depends on the EVALUATION/RUNTIME domains implementing the actual `apastra-audit` skill and integrating it into the run manifest/scorecard output.

#### 4. Test Plan
- **Verification**: Review the created `prompt-debt-governance.md` policy to ensure it clearly defines the boundaries of prompt debt and the blocking conditions for CI pipelines.
- **Success Criteria**: The policy document explicitly requires that new hardcoded prompts fail the governance gate and outlines an appeals process for necessary hardcoding (e.g., debug strings).
- **Edge Cases**: What happens if the audit skill incorrectly flags a normal code string as a prompt? The policy must allow for inline suppression comments or a `.promptopsignore` file.
