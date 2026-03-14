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
