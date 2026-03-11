# Context: EVALUATION

## Section A: Schema Inventory
Run Artifact Schema (from CONTRACTS) `promptops/schemas/run-artifact.schema.json`:
- `manifest`: input_refs, resolved_digests, timestamps, harness_version, model_ids, environment, status
- `scorecard`: normalized_metrics, metric_definitions
- `cases`: array of objects (case_id, per_trial_outputs, evaluator_outputs)
- `failures`: array of objects

Run Request Schema (from CONTRACTS) `promptops/schemas/run-request.schema.json`:
- `suite_id`: The benchmark suite ID
- `revision_ref`: The revision ref (SHA/tag/digest)
- `model_matrix`: Model matrix
- `evaluator_refs`: Evaluator references
- `trials`: Number of trials
- `budgets`: Budgets
- `timeouts`: Timeouts
- `artifact_backend_config`: Artifact backend config

Baseline Schema (from CONTRACTS) `promptops/schemas/baseline.schema.json`:
- `baseline_id`: The baseline ID
- `run_digest`: The run digest
- `created_at`: The creation time
- `metadata`: The metadata
- `description`: The description

## Section B: Validator Inventory
`promptops/runs/validate-run-request.sh`

## Section C: Source File Conventions
`promptops/harnesses/`
`promptops/runs/`
`promptops/runs/compare.py`
`derived-index/baselines/`
`derived-index/regressions/`

## Section D: Digest Convention
Follows the overall apastra PromptOps content digest convention (`sha256:<hex>`).

## Section E: Integration Points
GOVERNANCE reads regression reports and baseline digests to evaluate policy gates.
Currently blocked waiting for GOVERNANCE regression.yaml.

## Section F: Architecture
Harness execution flow:
- Run request generated and stored in `promptops/runs/<run-id>/run_request.json`
- Run request validated via `promptops/runs/validate-run-request.sh`
- Harness adapter invoked via entrypoint declared in `promptops/harnesses/<adapter-id>/adapter.yaml`
- Harness adapter consumes run request, resolves prompt using `promptops.runtime.resolve`, and generates `run_artifact.json`
- Scorecard normalizer `promptops/runs/normalize.py` parses evaluator outputs to update `scorecard.json` in `run_artifact.json`
- Regression report generated via `python promptops/runs/compare.py <candidate> <baseline> <policy> <output>`