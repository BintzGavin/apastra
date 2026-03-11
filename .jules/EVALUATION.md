# EVALUATION Journal

## 0.1.0 - Baseline Establishment Edge Case
**Learning:** Setting a baseline before any run artifact exists is impossible because baselines depend on existing scorecard data and immutable run artifact digests.
**Action:** The baseline establishment workflow must specify that the first run of any suite implicitly becomes the initial candidate or requires a manual bootstrap run.

## 0.1.0 - Cross-Domain Dependencies Missing
**Learning:** The run-request → artifact pipeline is blocked by missing CONTRACTS schemas (run-request.schema.json, run-artifact.schema.json, baseline.schema.json).
**Action:** Proceed to plan the Regression Comparison Engine, which relies on the GOVERNANCE policy file, until CONTRACTS delivers the schemas.
