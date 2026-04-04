# Capability Tagging Policy

## Overview
This policy governs how capability tags defined in the `suite.schema.json` are interpreted during the promotion process. Capability tags serve as an auditable link between test suite metadata and the governance promotion gates required for release.

## Tag Categories

### 1. Risk-Based Tags
Tags that denote high-risk execution or content.

- `risk:high-impact`: Indicates the suite involves core business logic or sensitive operations.
  - **Review Requirement**: Requires explicit approval from the `@promptops-core` CODEOWNERS team before promotion.
  - **Automated Gates**: All regression tests must pass with a 100% threshold.

- `risk:compliance`: Indicates the suite tests regulatory or compliance boundaries.
  - **Review Requirement**: Requires review by `@promptops-compliance` CODEOWNERS team.
  - **Automated Gates**: Must not be skipped under any execution tier.

### 2. Execution Characteristics
Tags that denote how the suite behaves during evaluation.

- `execution:costly`: Indicates the suite uses expensive model tiers or large datasets.
  - **Review Requirement**: Requires cost-budget approval if exceeding predefined limits.
  - **Automated Gates**: Cannot be run in `smoke` or `regression` tiers unless specifically triggered by budget overrides.

- `execution:flaky`: Indicates the suite contains non-deterministic tests known for intermittent failures.
  - **Review Requirement**: Warning flags raised to the PR author.
  - **Automated Gates**: Excluded from hard blocking regression gates, provided failures are documented in the PR context.

### 3. Subject Matter Domain
Tags indicating the core subject area of the evaluation suite.

- `domain:security`: Focuses on security, adversarial red-teaming, and jailbreak detection.
  - **Review Requirement**: Requires sign-off from `@promptops-security`.
- `domain:reasoning`: Focuses on complex reasoning, math, and logic tasks.
  - **Review Requirement**: Standard domain reviewer approval.

## Fallback Rule (Unregistered or Empty Tags)
If a suite contains no tags, or contains only unregistered tags not defined in this document:
- It will default to the **most restrictive review path**.
- It requires approval from a designated primary gatekeeper (`@promptops-gatekeepers`).
- Automated promotions are strictly disabled.
