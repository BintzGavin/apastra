# Role-Based Agent Skills Policy

## Purpose
This policy establishes the governance parameters and required capabilities for role-based agent skills (Review, Red-team, Optimize) to ensure rigorous and controlled prompt hardening.

## Required Parameters by Role

### Review ("Paranoid staff prompt engineer")
- **Injection Surface**: The skill must actively identify and alert on potential prompt injection vulnerabilities.
- **Variable Hygiene**: The skill must enforce strict variable typing and sanitation.
- **Format Contract Completeness**: The skill must verify that the prompt output adheres strictly to the defined schema.
- **Ambiguity**: The skill must flag ambiguous language that could lead to non-deterministic model behavior.

### Red-team ("Adversarial QA")
- **Multilingual Stress Tests**: The skill must test the prompt with inputs in multiple languages to ensure robustness.
- **Format-Breaking Inputs**: The skill must inject malformed or unexpected data structures to test error handling.
- **Prompt Injection Attempts**: The skill must actively attempt to bypass the prompt's instructions using known injection techniques.

### Optimize ("Performance engineer")
- **Token Usage Compression**: The skill must suggest refactoring to reduce token count without degrading evaluation performance.
- **Cost Reduction Estimation**: The skill must estimate the cost savings of the proposed optimizations.
- **Thresholds**: Optimizations must not cause the prompt to fail existing regression gates.

## Execution Context
The actual skills are provided by agent environments within RUNTIME, but this GOVERNANCE policy establishes the boundaries and validation thresholds. Results from these role-based skills act as preconditions for any results to be accepted in regression reports.
