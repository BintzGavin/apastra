# Prompt Debt Governance Policy

## 1. Overview
This policy establishes the acceptable limits and remediation requirements for "prompt debt" across the repository. Prompt debt is defined as any prompt string, template literal, or configuration that is hardcoded in application source code, unversioned within the `promptops/prompts/` directory, or untested against the core evaluation suites.

## 2. Policy Applicability
This governance applies to all pull requests modifying application source code or infrastructure configurations. It relies on the `apastra-audit` skill to identify and score prompt debt severity.

## 3. Thresholds and Gating Rules
The CI pipeline will enforce the following gating semantics based on the `apastra-audit` severity score:
- **Blocking Condition (Blocker):** Any pull request that introduces *new* prompt debt (i.e., increases the overall severity score compared to the baseline branch) will fail the governance gate.
- **Passing Condition:** Pull requests that reduce the overall prompt debt severity score, or maintain the existing baseline score without introducing new unversioned prompts, will pass the governance gate.
- **Baseline Exemption:** Legacy repositories with a pre-existing high prompt debt score will not be blocked from merging unrelated changes, provided the *new* debt delta is strictly zero or negative.

## 4. Remediation Requirements
All identified prompt debt must be remediated by:
1. Extracting the hardcoded string or template.
2. Creating a versioned prompt specification file in `promptops/prompts/`.
3. Updating the application source code to resolve the prompt dynamically using the PromptOps consumption manifest.
4. Implementing a minimum viable evaluation suite for the new prompt.

## 5. Appeals and Exceptions
In rare cases where a hardcoded prompt is strictly necessary (e.g., critical low-level debug strings or fail-safe bootstrap prompts), developers may request an exception by:
- Including an inline suppression comment (e.g., `// promptops-ignore: reason`) or updating the `.promptopsignore` file.
- Securing explicit approval from the `@apastra/governance-admins` CODEOWNERS group.
