# Dataset Holdout Sets Policy

## 1. Purpose and Scope
To prevent overfitting and benchmark gaming, all release candidate suites MUST utilize dedicated holdout datasets. This policy establishes the governance expectations for dataset holdouts during pre-release validation.

## 2. Definition of a Valid Holdout Set
A valid holdout set is a versioned dataset (e.g., JSONL) that:
- Is distinct and isolated from datasets used for routine developer iteration and training.
- Accurately represents the target distribution of inputs the prompt or model will encounter in production.
- Contains sufficient examples to provide statistical confidence in the evaluation metrics.

## 3. Requirements
- **Release Candidates:** All suites designated as release candidates must include at least one valid holdout set in their configuration.
- **Exclusion from Iteration:** Holdout datasets must not be used during routine development, prompt engineering, or model fine-tuning to maintain their integrity as an unbiased evaluation standard.
- **Policy Enforcement:** The regression policy engine will evaluate release candidates against these holdout sets. Promotion to production channels requires passing results on the holdout sets.
- **Promotion Records:** Promotion records must explicitly reflect the evaluation results against the designated holdout sets for release candidates.

## 4. Maintenance and Rotation
- **Rotation:** Holdout sets should be periodically rotated or updated to prevent gradual overfitting over time (e.g., when the production data distribution shifts).
- **Integrity:** When a holdout set is updated, the previous version should be preserved to maintain the integrity and comparability of historical benchmarks.
