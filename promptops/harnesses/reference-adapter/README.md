# Retired reference adapter

This compatibility entry point exits with `unsupported` and emits no results.
Its former synthetic scores, cases, and cost estimates were not evaluation evidence.

Use an explicit measured adapter implementing the [execution contract](../../../docs/guides/evaluation-trust.md).
The adapter must actually execute the requested target and evaluator, report every
model/case/trial, and retain their results. The runner recomputes aggregate metrics
and applies the suite policy. A zero process exit alone never constitutes a pass.

Apastra does not bundle a live-provider or framework execution adapter. The
deterministic target in the test suite proves the protocol, not LLM quality.
