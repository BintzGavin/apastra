# EVALUATION Domain Context

## Section A: Architecture
The execution engine receives a `run_request.json` defining a test suite. It resolves dependencies, triggers the harness adapter per `evaluate_assertions.py`, and generates a unified test summary in a `run_artifact.json`. It can produce `scorecard.json` metrics for external policy gates.

## Section B: File Tree
```
promptops/
├── harnesses/                  # Harness adapter implementations
│   └── <adapter-id>/
│       ├── adapter.yaml
│       └── run.ts
└── runs/                       # Run requests and artifacts
    └── <run-id>/
        ├── run_request.json
        ├── run_artifact.json
        ├── scorecard.json
        ├── cases.jsonl
        └── artifact_refs.json

derived-index/
├── baselines/                  # Named baselines
│   └── <baseline-id>.json
└── regressions/                # Regression reports
    └── <report-id>.json
```

## Section C: Run Artifact Format
**run_artifact.json**
- `run_id` (string, required)
- `dataset_digest` (string, required)
- `harness_version` (string, required)
- `metrics` (object, optional)
- `digest` (string, required) - sha256 of content

**scorecard.json**
- `run_id` (string, required)
- `metrics` (object, required)
- `pass` (boolean, required)

## Section D: Baseline and Regression Format
**Baseline** (`<baseline-id>.json`)
- `run_id` (string, required)
- `digest` (string, required)
- `scorecard` (object, required)

**Regression Report** (`<report-id>.json`)
- `candidate_id` (string, required)
- `baseline_id` (string, required)
- `delta` (object, required)
- `pass` (boolean, required)

## Section E: Integration Points
- **GOVERNANCE**: Reads `<report-id>.json` and `<baseline-id>.json` digests to make automated deployment/promotion decisions based on policy thresholds.
