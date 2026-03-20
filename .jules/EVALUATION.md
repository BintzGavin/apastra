# EVALUATION Journal

## 0.1.0 - Baseline Establishment Edge Case
**Learning:** Setting a baseline before any run artifact exists is impossible because baselines depend on existing scorecard data and immutable run artifact digests.
**Action:** The baseline establishment workflow must specify that the first run of any suite implicitly becomes the initial candidate or requires a manual bootstrap run.

## 0.1.0 - Cross-Domain Dependencies Missing
**Learning:** The run-request → artifact pipeline is blocked by missing CONTRACTS schemas (run-request.schema.json, run-artifact.schema.json, baseline.schema.json).
**Action:** Proceed to plan the Regression Comparison Engine, which relies on the GOVERNANCE policy file, until CONTRACTS delivers the schemas.

## 0.6.0 - Scorecard Normalization
**Learning:** Successfully implemented scorecard normalizer to extract normalized metrics from case evaluator outputs. Discovered that the normalizer requires valid numeric scores in evaluator_outputs to function correctly.
**Action:** Implemented metric aggregation and averaging in normalize.py, integrated securely via subprocess in the reference adapter.

## 0.8.0 - Scorecard Normalization Architecture Mismatch
**Learning:** Discovered that the Scorecard Normalizer (`promptops/runs/normalize.py`) currently injects a scorecard object back into a monolithic artifact JSON file, modifying it in place. This violates the new append-friendly artifacts branch architecture.
**Action:** The Scorecard Normalizer must be refactored to read from `cases.jsonl` and output a separate, distinct `scorecard.json` file.

## 0.11.0 - Harness Adapter Inconsistency
**Learning:** The reference harness adapter (`promptops/harnesses/reference-adapter/run.py`) outputs a monolithic `run_artifact.json` and incorrectly calls the refactored `normalize.py`. This causes an inconsistency with the new append-friendly split-artifact architecture expected by the RUNTIME runner shim.
**Action:** The reference adapter must be refactored to write `run_manifest.json`, `cases.jsonl`, `failures.json`, and `artifact_refs.json` directly, and pass the correct file paths to the normalizer.
## [0.15.0] - ModelAssistedAssertions
**Learning:** Deterministic evaluation requires temporary placeholder scores for model-assisted capabilities.
**Action:** Revisit evaluate_assertions when LLM rubric scoring is fully supported.

## [0.16.0] - TrialsAndVarianceSupport
**Learning:** Found that `normalize.py` computes an average score across all evaluator outputs without recording variance, and `run.py` ignores the `trials` parameter in the run request. This prevents variance-aware regression gating.
**Action:** Spec'd the implementation of variance calculation in `normalize.py` and trial looping in `run.py` to support non-deterministic evaluators.

## [0.16.0] - JsonSchemaAssertion
**Learning:** Found that `evaluate_assertions.py` lacks implementation for `is-valid-json-schema`, causing inline assertions of this type to silently fall through to the default failure case.
**Action:** Spec'd the implementation of `is-valid-json-schema` evaluation logic, utilizing `extract_json_blocks` and `jsonschema` validation against the provided schema value.

## [0.36.0] - Minimal Plan Exception Final
**Learning:** The EVALUATION domain has already executed its final minimal plan exception.
**Action:** Proceeded with no-op exception.

## 0.42.0 - Minimal Plan Exception Final
**Learning:** The EVALUATION domain has already executed its final minimal plan exception.
**Action:** Proceeded with no-op exception.

## [v0.44.0] - Minimal Plan Exception Final
**Learning:** Reached the end of functional planning iterations; all planned domain features are marked completed.
**Action:** Log a minimal plan exception to fulfill system planning requirements.

## [v0.50.0] - Minimal Plan Exception Final
**Learning:** Reached the end of functional planning iterations; all planned domain features are marked completed.
**Action:** Log a minimal plan exception to fulfill system planning requirements.

## [v0.57.0] - Minimal Plan Exception Final
**Learning:** The EVALUATION domain has already executed its final minimal plan exception.
**Action:** Proceeded with no-op exception.

## [v0.58.0] - Minimal Plan Exception Final
**Learning:** The EVALUATION domain has already executed its final minimal plan exception.
**Action:** Proceeded with no-op exception.

## [v0.59.0] - Minimal Plan Exception Final
**Learning:** The EVALUATION domain has already executed its final minimal plan exception.
**Action:** Proceeded with no-op exception.

## [0.64.0] - Minimal Plan Exception Final
**Learning:** The EVALUATION domain has already executed its final minimal plan exception.
**Action:** Proceeded with no-op exception.

## [0.65.0] - Minimal Plan Exception Final
**Learning:** The EVALUATION domain has already executed its final minimal plan exception.
**Action:** Proceeded with no-op exception.
## [v0.65.0] - Minimal Plan Exception
**Learning:** System planning requirements fulfilled because all functional planning iterations are marked completed.
**Action:** Execute minimal plan exception as instructed.

## [v0.66.0] - Minimal Plan Exception
**Learning:** System planning requirements fulfilled because all functional planning iterations are marked completed.
**Action:** Execute minimal plan exception as instructed.

## [v0.67.0] - Minimal Plan Exception
**Learning:** System planning requirements fulfilled because all functional planning iterations are marked completed.
**Action:** Execute minimal plan exception as instructed.

## [v0.68.0] - MinimalPlanExceptionFinal
**Learning:** None
**Action:** None

## 0.69.0 - MinimalPlanExceptionFinal
**Learning:** None
**Action:** None

## 0.70.0 - MinimalPlanExceptionFinal
**Learning:** None
**Action:** None

## 0.71.0 - MinimalPlanExceptionFinal
**Learning:** None
**Action:** None

## 0.72.0 - MinimalPlanExceptionFinal
**Learning:** None
**Action:** None

## 0.73.0 - MinimalPlanExceptionFinal
**Learning:** None
**Action:** None

## 0.74.0 - MinimalPlanExceptionFinal
**Learning:** None
**Action:** None

## 0.75.0 - MinimalPlanExceptionFinal
**Learning:** None
**Action:** None

## 0.76.0 - MinimalPlanExceptionFinal
**Learning:** None
**Action:** None

## [v0.77.0] - Tradeoff Surfacing
**Learning:** Surfacing ungated metrics provides valuable context for human review without enforcing policy gates.
**Action:** Iterate on regression report schema and frontend integration to better surface 'info' status evidence.

## 0.78.0 - MinimalPlanExceptionFinal
**Learning:** None
**Action:** None

## 0.79.0 - MinimalPlanExceptionFinal
**Learning:** None
**Action:** None

## 0.80.0 - MinimalPlanExceptionFinal
**Learning:** None
**Action:** None

## 0.81.0 - AnswerRelevanceAssertion
**Learning:** Found that `evaluate_assertions.py` lacks an implementation for `answer-relevance`, currently returning a placeholder score.
**Action:** Spec'd the implementation of `answer-relevance` evaluation logic.
