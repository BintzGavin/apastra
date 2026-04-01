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

## [v0.77.0] - Tradeoff Surfacing
**Learning:** Surfacing ungated metrics provides valuable context for human review without enforcing policy gates.
**Action:** Iterate on regression report schema and frontend integration to better surface 'info' status evidence.

## 0.81.0 - AnswerRelevanceAssertion
**Learning:** Found that `evaluate_assertions.py` lacks an implementation for `answer-relevance`, currently returning a placeholder score.
**Action:** Spec'd the implementation of `answer-relevance` evaluation logic.

## 0.83.0 - LLMRubricAssertion
**Learning:** Found that `evaluate_assertions.py` lacks an implementation for `llm-rubric`, currently returning a placeholder score.
**Action:** Spec'd the implementation of `llm-rubric` evaluation logic.

## 0.91.0 - RunRequestDigestValidation
**Learning**: The Run Request schema currently lacks required fields for tracking inputs such as prompt digest, dataset digest, and evaluator digest. This metadata is essential for reproducibility as per the vision documentation.
**Action**: Created a plan spec to explicitly define the necessary updates for the Run Request schema in the CONTRACTS domain.

## 0.26.0 - PromptReviewWorkflow
**Learning:** Discovered the need for automated prompt reviews to catch foundational prompt issues before evaluation suites are run.
**Action:** Implemented a prompt review evaluation yaml using llm-rubric assertions.

## [v0.26.0] - AuditSkillExecution
**Learning:** Discovered the need for an Audit Skill execution flow to scan codebases for prompt debt as defined in the vision docs.
**Action:** Spec'd the implementation of audit-shim.sh to generate audit_report.json.

## 0.40.14 - Minimal Plan Exceptions
**Learning:** Found several specs (LLMRubricAssertion, FactualityAssertion, SimilarAssertion, RunRequestDigestValidation series, DriftDetectionCanaryShim, CommunityPromptPacks, ProjectLevelConfigAndMinimalMode, MinimalModeSupport, v0.49.0) whose functional intent is already present in the codebase.
**Action:** Logged as minimal plan exceptions and updated domain status properly.
