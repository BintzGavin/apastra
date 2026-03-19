# Context: EVALUATION

## Section A: Architecture
Harness execution flow:
- (Quick Eval Mode) `promptops/runs/quick-eval.sh <yaml>` dynamically constructs a run request and dataset from a yaml file before invoking the harness.
- Run request generated   and stored in `promptops/runs/<run-id>/run_request.json`
- Run request validated via `promptops/runs/validate-run-request.sh`
- Harness adapter invoked via entrypoint declared in `promptops/harnesses/<adapter-id>/adapter.yaml`
- Harness adapter co n s umes run request, resolves prompt using `promptops.runtime.resolve`, and generates split artifacts natively (`run_manifest.json`, `cases.jsonl`, `failures.json`, `artifact_refs.json`). It natively enforces `budgets` and `timeouts`.
- If inline a  s se rt ions are used, the adapter leverages `promptops/runs/evaluate_assertions.py` to deterministically calculate per-case pass/fail scores. This also supports model-assisted, performance assertions (latency, cost), and `is-valid-json-schema` asse rti on  typ es.
- Scorecard normalizer `promptops/runs/normalize.py` parses evaluator outputs from `cases.jsonl` and writes a distinct `scorecard.json` file.
- Regression report generated and stored via `promptops/runs/generate_regression_report.sh <cand idat e> < baseline> <policy> <report_id>`, with ungated metrics surfaced as informational evidence.

## Section B: File Tree
- `promptops/harnesses/`
- `promptops/runs/`
  - `promptops/runs/compare.py`
  - `promptops/runs/evaluate_assertions.py `
  -  `prom ptops /runs/normalize.py`
- `derived-index/baselines/`
- `derived-index/regressions/`

## Section C: Run Artifact Format
Run Artifact Schema (from CONTRACTS) `promptops/schemas/run-artifact.schema.json`:
- `manifest`: input_refs, resolved_diges ts, ti mestam ps, harness_version, model_ids, environment, status, provenance
- `scorecard`: normalized_metrics, metric_definitions (including versioning), variance, flake_rates
- `cases`: array of objects (case_id, per_trial_outputs, evaluato r_outpu ts)
- ` failure s`: array of objects

## Section D: Baseline and Regression Format
Baseline Schema (from CONTRACTS) `promptops/schemas/baseline.schema.json`:
- `baseline_id`: The baseline ID
- `run_digest`: The run digest
- `created_at`: Th  e  c reation  time
- `metadat a`: The metadata
- `description`: The description

## Section E: Integration Points
GOVERNANCE reads:
- `derived-index/regressions/<report-id>.json` to evaluate policy gates (e.g. `status` field for pass/fail/warning decisions).
- `d erived-i ndex/base lines/<baseline-id>.json` to find the `run_digest` needed to locate the baseline's `scorecard.json`
