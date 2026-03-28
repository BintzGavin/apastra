# Multi-Model Promotion Policy

## 1. Context and Scope
This policy governs the evaluation and promotion of specific model and prompt combinations resulting from multi-model comparison scorecards. It ensures that tradeoffs between quality, cost, and latency are explicitly evaluated and recorded.

## 2. Multi-Model Scorecards
When an evaluation suite utilizes a `model_matrix` to test a prompt across multiple models simultaneously, the resulting scorecard MUST clearly delineate the performance metrics (quality, cost, latency) for each `model_id`.

## 3. Promotion Criteria
To promote a prompt package evaluated via a multi-model suite:
- The promotion record MUST explicitly declare the selected `model_id`.
- The selected `model_id` MUST meet all baseline quality thresholds defined in the suite's `pass_rate` or specific metric assertions.
- **Tradeoff Review**: If the selected model fails to achieve the highest quality score among the candidates but is selected for cost or latency optimizations, the promotion PR MUST include a written justification and requires approval from `@apastra/governance-admins`.

## 4. Promotion Record Format
All derived promotion records for multi-model suites MUST include the `model_id` field in the append-only registry metadata store, permanently associating the approved prompt digest with the selected target model.

## 5. Auditability
All multi-model promotion decisions, including the associated multi-model scorecards and tradeoff justifications, are strictly append-only and fully auditable.
