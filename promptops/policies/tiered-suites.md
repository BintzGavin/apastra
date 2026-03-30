# Tiered Evaluation Suites Policy

## 1. Context and Purpose
To mitigate the risk of "false confidence" (narrow evaluation suites missing real-world failures), all evaluation suites MUST be categorized into strict tiers. This document defines the required suite tiering hierarchy, the mandatory test mix for each tier, and the strict gating rules for promotion into production environments.

## 2. Evaluation Suite Tiers

### 2.1 Smoke Tier
- **Purpose**: Fast developer iteration and rapid feedback during local development.
- **Scope**: Minimal dataset covering basic functionality and syntax correctness.
- **Execution**: Run locally by developers.
- **Gating**: Does not gate PR merges or production promotions.

### 2.2 Regression Tier
- **Purpose**: Prevent regressions on core capabilities during pull requests.
- **Scope**: A comprehensive subset of test cases representing critical capabilities, derived from historical failures and core product requirements.
- **Execution**: Automatically executed in CI/CD pipelines for all Pull Requests affecting evaluable assets.
- **Gating**: Must pass for a PR to be merged into the main branch (`regression-gate.yml`).

### 2.3 Release-Candidate Tier
- **Purpose**: Exhaustive validation of all capabilities before promotion to production.
- **Scope**: The complete, comprehensive evaluation suite, including extensive capability tagging and holdout sets.
- **Execution**: Automatically executed against release candidates.
- **Gating**: Mandatory for any promotion. `promote.yml` and `immutable-release.yml` MUST verify that the baseline passed the Release-Candidate tier before appending a promotion record.

## 3. Promotion Requirements
1. The referenced `evidence.run_id` in any promotion record MUST originate from a documented Release-Candidate suite execution.
2. The EVALUATION domain is responsible for exposing a `tier` or `tags` array in the suite schema (`suite.schema.json`) to programmatically label suites as `release-candidate` or `regression`.
3. Bypass of the Release-Candidate gate is strictly prohibited, except under documented Emergency Hotfix procedures.

## 4. Emergency Exceptions
In the event of an emergency hotfix, a documented exception must be filed, and the regression tier may temporarily suffice for promotion, pending a post-incident Release-Candidate execution.
