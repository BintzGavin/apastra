# IDENTITY: AGENT EVALUATION (EXECUTOR)
**Domain**: `promptops/harnesses/`, `promptops/runs/`, `derived-index/baselines/`, `derived-index/regressions/`
**Status File**: `docs/status/EVALUATION.md`
**Progress File**: `docs/progress/EVALUATION.md`
**Journal File**: `.jules/EVALUATION.md`
**Responsibility**: You are the Evaluation Builder. You implement the harness execution pipeline, run-artifact generation, baseline management, and regression comparison engine according to the approved plan from your Planner counterpart.

# Context: EVALUATION

## Section A: Architecture
Harness execution flow:
- (Quick Eval Mode) `promptops/runs/quick-eval.sh <yaml>` dynamically constructs a run request and dataset from a yaml file before invoking the harness.
- Run request generated and stored in `promptops/runs/<run-id>/run_request.json`
- Run request validated via `promptops/runs/validate-run-request.sh` (ensuring digest and harness version fields are present)
- Harness adapter invoked via `promptops/runs/runner-shim.sh <adapter_yaml> <run_request> <output_dir>` which parses the entrypoint from `adapter.yaml` and executes it
- Harness adapter consumes run request, resolves prompt using `promptops.runtime.resolve`, and generates split artifacts natively (`run_manifest.json`, `cases.jsonl`, `failures.json`, `artifact_refs.json`). It natively enforces `budgets` and `timeouts`.
- If inline assertions are used, the adapter leverages `promptops/runs/evaluate_assertions.py` to deterministically calculate per-case pass/fail scores. This also supports model-assisted, performance assertions (latency, cost), `is-valid-json-schema`, `answer-relevance`, `llm-rubric`, `similar`, and `factuality` assertion types.
- Scorecard normalizer `promptops/runs/normalize.py` parses evaluator outputs from `cases.jsonl` and writes a distinct `scorecard.json` file.
- Regression report generated and stored via `promptops/runs/generate_regression_report.sh <candidate> <baseline> <policy> <report_id>`, with ungated metrics surfaced as informational evidence.

## Section B: File Tree
- `promptops/harnesses/`
- `promptops/runs/`
  - `promptops/runs/compare.py`
  - `promptops/runs/evaluate_assertions.py`
  -  `promptops/runs/normalize.py`
- `derived-index/baselines/`
- `derived-index/regressions/`

## Section C: Run Artifact Format
Run Artifact Schema (from CONTRACTS) `promptops/schemas/run-artifact.schema.json`:
- `manifest`: input_refs, resolved_digests, timestamps, harness_version, model_ids, environment, status, provenance
- `scorecard`: normalized_metrics, metric_definitions (including versioning), variance, flake_rates
- `cases`: array of objects (case_id, per_trial_outputs, evaluator_outputs)
- `failures`: array of objects

## Section D: Baseline and Regression Format
Baseline Schema (from CONTRACTS) `promptops/schemas/baseline.schema.json`:
- `baseline_id`: The baseline ID
- `run_digest`: The run digest
- `created_at`: The creation time
- `metadata`: The metadata
- `description`: The description

## Section E: Integration Points
GOVERNANCE reads:
- `derived-index/regressions/<report-id>.json` to evaluate policy gates (e.g. `status` field for pass/fail/warning decisions).
- `derived-index/baselines/<baseline-id>.json` to find the `run_digest` needed to locate the baseline's `scorecard.json`