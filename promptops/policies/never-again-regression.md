# Never Again Regression Policy

## 1. Objective
This policy defines the governance for promoting production incidents into a mandatory "never again" regression suite, preventing the recurrence of previously resolved issues.

## 2. Policy Requirements

- **Mandatory Inclusion**: Any production incident resulting from a prompt failure requires at least one new test case added to a designated never-again dataset.
- **Mandatory Execution**: The never-again dataset must be included in a mandatory suite (e.g., never-again-suite) that runs on every PR and promotion.
- **Strict Threshold**: The never-again-suite must have a strict 1.0 (100%) pass rate threshold in the regression policy configuration. No regressions or flakiness are permitted.

## 3. Incident Response Workflow

After a production incident related to a prompt failure, the following steps must be taken:

1.  **Identify Failure**: Analyze the incident to understand the specific input and the incorrect model output.
2.  **Write Minimal Reproducible Case**: Create a minimal dataset case that reproduces the failure.
3.  **Assert Correct Behavior**: Define the expected, correct behavior using an appropriate evaluator and assertion.
4.  **Add to Dataset**: Add the new test case to the never-again dataset.

## 4. Edge Cases: Non-Determinism and Quarantine

If an incident cannot be reliably reproduced due to model provider non-determinism, the test case should still be created. However, if the flakiness is consistently high and prevents merges, the case may be temporarily moved to a quarantine state for further investigation, provided a tracking issue is created.
