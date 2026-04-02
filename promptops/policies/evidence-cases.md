# Evidence Cases Policy

This policy implements the "require evidence cases" governance requirement to prevent benchmark gaming.

When evaluating models or suites, teams may optimize for the benchmark score. To mitigate this, evaluation suites and pull requests must include explicit evidence cases (e.g. traced dataset inputs/outputs) to prove claims.

This prevents the optimization of aggregate scores without providing the necessary qualitative proof.

- Evaluators MUST include clear assertions or raw artifact links for edge cases and subjective evidence.
- Pull requests modifying core capabilities MUST link to the trace or dataset case that serves as evidence.
