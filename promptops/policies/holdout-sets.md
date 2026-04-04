# Holdout Sets Policy

## 1. Purpose
This policy establishes governance requirements for the use of holdout datasets during the release candidate validation process. Its primary objective is to prevent overfitting and "benchmark gaming" by ensuring that models and prompts are evaluated against unseen data before promotion to production.

## 2. Applicability
This policy applies to all validation suites designated as "release candidates" across all domains.

## 3. Policy Rules

### 3.1. Requirement of Holdout Sets
All suites designated as release candidates MUST be validated against a designated holdout set before they can be considered for promotion.

### 3.2. Integrity of Holdout Sets
Holdout datasets MUST be strictly excluded from routine developer iteration, training, and quick-eval pipelines. They are reserved exclusively for final release candidate validation.

### 3.3. Evaluation Enforcement
The regression policy engine MUST evaluate release candidates against the designated holdout sets. A passing result against the holdout set is a hard requirement for promotion.

### 3.4. Promotion Records
Promotion records MUST explicitly reflect passing validation results against the required holdout sets. A promotion record lacking this evidence is considered invalid.

### 3.5. Rotation and Refresh
Holdout sets should be periodically rotated or refreshed to maintain their effectiveness as an unseen validation benchmark. When rotating, care must be taken to maintain the integrity and comparability of historical benchmarks where feasible.

## 4. Enforcement
This policy is enforced mechanically via the regression policy engine and promotion workflow constraints. Any attempt to bypass holdout evaluation for a release candidate will result in a blocked promotion.
