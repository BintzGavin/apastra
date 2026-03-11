# Context: EVALUATION

## Section A: Schema Inventory
Run Artifact Schema (from CONTRACTS) `promptops/schemas/run-artifact.schema.json`:
- `manifest`: input_refs, resolved_digests, timestamps, harness_version, model_ids, environment, status
- `scorecard`: normalized_metrics, metric_definitions
- `cases`: array of objects (case_id, per_trial_outputs, evaluator_outputs)
- `failures`: array of objects

## Section B: Validator Inventory
No validators defined locally; delegates to CONTRACTS domain validators.

## Section C: Source File Conventions
`promptops/harnesses/`
`promptops/runs/`
`derived-index/baselines/`
`derived-index/regressions/`

## Section D: Digest Convention
Follows the overall apastra PromptOps content digest convention (`sha256:<hex>`).

## Section E: Integration Points
GOVERNANCE reads regression reports and baseline digests to evaluate policy gates.
Currently blocked waiting for CONTRACTS baseline.schema.json and GOVERNANCE regression.yaml.
