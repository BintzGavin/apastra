# Flake Quarantine Policy

## 1. Objective
This policy defines the governance rules for isolating and managing flaky evaluation cases to prevent false-positive regression alerts without letting flakiness pass as random noise.

## 2. Definition of Flakiness
A test case is considered "flaky" if it exhibits inconsistent pass/fail results across multiple trials without any changes to the underlying prompt or evaluator logic.

## 3. Quarantine Process
- Flaky cases MUST be temporarily isolated into a designated "quarantine" dataset or explicitly marked as quarantined in their metadata.
- Quarantined cases MUST NOT block promotions or trigger regression gates while under active investigation.

## 4. Remediation and Tracking
- Teams MUST track the flake rate of quarantined cases.
- Flakiness must be resolved (e.g., by improving evaluator logic, refining the prompt, or fixing non-determinism) before the case can be reinstated into the blocking regression suite.
- Quarantining a case is a temporary measure and NOT a permanent bypass.
