# EVALUATION Domain Context

## Section A: Architecture
The EVALUATION domain executes run requests to generate append-only run artifacts.
- **Run Request Validation**: `validate-run-request.sh` ensures `prompt_digest`, `dataset_digest`, `evaluator_digest`, and `harness_version` are present.
- **Run Artifact Generation**: Monolithic `run_artifact.json` is split into `run_manifest.json`, `cases.jsonl`, `failures.json`, and `artifact_refs.json` for append-only storage.
- **Scorecard Normalization**: Extracts normalized metrics from case evaluator outputs and calculates variance across trials. Outputs `scorecard.json`.
- **Regression Report Generator**: `generate_regression_report.sh` compares the generated `scorecard.json` against a stored baseline and issues a pass/fail.

## Section B: File Tree
```
promptops/
├── harnesses/
│   └── reference-adapter/
│       ├── adapter.yaml
│       └── run.py
└── runs/
    ├── <run-id>/
    │   ├── run_request.json
    │   ├── run_manifest.json
    │   ├── cases.jsonl
    │   ├── failures.json
    │   ├── artifact_refs.json
    │   └── scorecard.json
    ├── validate-run-request.sh
    ├── runner-shim.sh
    ├── split_artifact.sh
    ├── normalize.py
    ├── establish_baseline.sh
    └── generate_regression_report.sh

derived-index/
├── baselines/
│   └── <suite-id>.json
└── regressions/
    └── <report-id>.json
```

## Section C: Run Artifact Format
- **`run_manifest.json`**: Contains digests (`prompt_digest`, `dataset_digest`, `evaluator_digest`), `harness_version`, `model_ids`, and `sampling_config`.
- **`scorecard.json`**: Contains aggregated `metrics` (value, threshold, pass/fail status).
- **`cases.jsonl`**: Individual case records.
- **`failures.json`**: Case failures.
- **`artifact_refs.json`**: Large raw outputs.

## Section D: Baseline and Regression Format
- **Baseline**: `derived-index/baselines/<suite-id>.json` contains `baseline_run_id`, `digest`, and a `scorecard` snapshot. Written once, never overwritten.
- **Regression Report**: `derived-index/regressions/<report-id>.json` contains candidate vs. baseline scorecard metrics. Contains pass/fail status based on policy gates.

## Section E: Integration Points
GOVERNANCE reads:
- `derived-index/regressions/<report-id>.json` to gate promotions based on pass/fail status.
- `derived-index/baselines/<suite-id>.json` digests to verify what candidate runs were compared against.
