# Context: EVALUATION

## Section A: Architecture
Harness execution flow:
- Run request generated and stored in `promptops/runs/<run-id>/run_request.json`
- Run request validated via `promptops/runs/validate-run-request.sh`
- Harness adapter invoked via entrypoint declared in `promptops/harnesses/<adapter-id>/adapter.yaml`
- Harness adapter consumes run request, resolves prompt using `promptops.runtime.resolve`, and generates split artifacts natively (`run_manifest.json`, `cases.jsonl`, `failures.json`, `artifact_refs.json`).
- Scorecard normalizer `promptops/runs/normalize.py` parses evaluator outputs from `cases.jsonl` and writes a distinct `scorecard.json` file
- Regression report generated and stored via `promptops/runs/generate_regression_report.sh <candidate> <baseline> <policy> <report_id>`

## Section B: File Tree
`promptops/harnesses/`
`promptops/runs/`
`promptops/runs/compare.py`
`derived-index/baselines/`
`derived-index/regressions/`

## Section C: Run Artifact Format
Run Artifact Schema (from CONTRACTS) `promptops/schemas/run-artifact.schema.json`:
- `manifest`: input_refs, resolved_digests, timestamps, harness_version, model_ids, environment, status
- `scorecard`: normalized_metrics, metric_definitions
- `cases`: array of objects (case_id, per_trial_outputs, evaluator_outputs)
- `failures`: array of objects

## Section D: Baseline and Regression Format
Baseline Schema (from CONTRACTS) `promptops/schemas/baseline.schema.json`:
- `baseline_id`: The baseline ID
- `run_digest`: The run digest
- `created_at`: The creation time
- `metadata`: The metadata
- `description`: The description
