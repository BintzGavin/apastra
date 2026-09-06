---
name: apastra-eval
description: Execute a declared harness, validate complete measured evidence, and apply explicit suite or quick-eval criteria.
---

# Apastra eval

Find the requested suite or quick-eval file and the operator's measured adapter.
An agent-driven execution must expose a real executable adapter implementing the
same contract. When no adapter exists, report `unsupported` and identify the
missing execution capability.

## Execute

```bash
.agent/bin/apastra eval smoke --adapter promptops/harnesses/local.yaml --output-dir promptops/runs/candidate
.agent/bin/apastra quick-eval promptops/evals/smoke.yaml --adapter promptops/harnesses/local.yaml --models model-a --output-dir promptops/runs/quick
.agent/bin/apastra compare smoke --adapter promptops/harnesses/local.yaml --models model-a model-b --output-dir promptops/runs/comparison
```

Use a new output directory for every invocation. Preserve diagnostics when a
command fails. Return the command's verdict and evidence path to the user.

The runner resolves input snapshots and checks their digests. It requires the
complete requested model/case/trial set and finite scores for every declared
metric, then recomputes means before applying the suite's criteria. Metric
definitions carry a version, direction, and unit.

A completed target can fail a quality criterion. A subprocess exit code or a
schema-validation result is insufficient to claim an evaluation pass. Empty
criteria produce `not_evaluated`, which cannot establish a baseline.

## Adapter responsibilities

Read the full [execution contract](../docs/guides/evaluation-trust.md) before
building an adapter. The adapter must execute the specified target and evaluator,
capture outputs for every trial, and emit all required files. Only invoke code
approved by the operator.

For built-in assertions, use:

```bash
python .agent/scripts/apastra/runs/evaluate_assertions.py output.txt assertions.json
```

Model-assisted assertions need an explicit callable judge through the Python API.
Missing measurements or invalid evaluator results are errors. Negation only
applies to valid boolean outcomes.

To normalize complete per-trial scores, supply an explicit metric-definition
map:

```bash
python .agent/scripts/apastra/runs/normalize.py cases.jsonl metric-definitions.json scorecard.json
```

Quick evals declare `pass_rate`: a trial passes only when all assertions pass.
Compute the mean over every requested trial. Evaluator errors make the run
ineligible for admission.

## Retain evidence and compare

Required adapter files are `run_manifest.json`, `cases.jsonl`, `scorecard.json`,
and `artifact_refs.json`. The runner adds the resolved request, invocation
record, and evaluation outcome. Extra artifact references identify retained local
files by their raw-byte digests.

```bash
.agent/bin/apastra gate promptops/runs/candidate --baseline promptops/runs/accepted --policy promptops/policies/regression.yaml --adapter promptops/harnesses/local.yaml
```

Choose a baseline explicitly. Follow the baseline skill when the user wants to
establish one, preserving earlier named records.

## Designing useful cases

Follow `apastra-writing-evals` for interactive design. Prefer observed failures
and include a failing control case. Separate outcome evidence from critical
steps when the execution path matters. Keep private transcripts and credentials
out of committed evidence.

Judge calibration and live-provider integrations need their own validation.
The deterministic acceptance target shipped in the tests proves the protocol
without claiming model quality.
