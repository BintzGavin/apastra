---
title: "Harness Contract"
description: "Understanding the minimal BYO harness contract"
audience: "developers | platform-teams | agents"
last_verified: "2026-04-01"
source_files:
  - "README.md"
---

# Harness Contract

The core of the PromptOps system is its Bring-Your-Own (BYO) compute execution model. Instead of relying on a hosted SaaS platform, the system relies on a strict but minimal "run request in, run artifact out" file-based contract.

## Purpose

This decoupling mechanism empowers teams to choose their compute layer—be it a simple Python script, a complex internal scheduler, or an existing evaluation framework (e.g., OpenAI Evals, promptfoo). So long as the harness adheres to the inputs and expected outputs of the contract, the rest of the PromptOps system remains stable and vendor-agnostic.

## Required Inputs

When the evaluation engine generates a benchmark execution order, it emits a `run_request.json` (or YAML) file.

The harness receives:
- The `run_request.json` specification:
  - Suite ID
  - Revision reference (SHA, tag, or digest)
  - Model matrix
  - Trials, budgets, timeouts
  - Evaluator references
  - Artifact backend configuration
- The resolved prompt package, or instructions for a resolver to materialize the source files.
- An output directory path for generated artifacts.

## Harness Responsibilities

The execution environment must accomplish the following:

1. **Honor Resolved Inputs:** Use the immutable input snapshots and digests in the request produced by Apastra.
2. **Execute Suites:** Process the benchmark suite across the specified datasets and model matrix.
3. **Apply Evaluators:** Evaluate the outputs and produce consistent metrics.
4. **Emit Run Artifacts:** Populate the structured run artifact directory.
5. **Attach Raw Traces:** Attach references (URIs) and digests to raw text, logs, and traces.
6. **Record Environment Metadata:** Capture data required to reproduce the run (harness identifier, harness version, model IDs, sampling configurations). The harness identifier (e.g., `claude-code`, `antigravity`, `cursor`, `api`) is a required field distinct from the model ID, since the same model can behave differently across execution environments.

## Required Outputs

The harness must generate the following standard structures inside the artifact directory:

### `run_manifest.json`
A comprehensive metadata record. It must contain the harness identifier (e.g., `claude-code`, `antigravity`, `cursor`, `api`, `github-actions`), resolved digests, timestamps, harness version, model IDs, sampling configs, environment data, and the overall status.

### `scorecard.json`
The normalized evaluation results. This file holds the metrics, metric definitions, metric versioning, and optional descriptive trial variance data (the runtime recomputes means, not variance).

### `cases.jsonl`
A detailed per-case record file. It must include stable case IDs, per-trial outputs, evaluation outputs, and pointers to raw artifacts (traces, text).

### `artifact_refs.json`
A manifest of URIs and corresponding digests referencing the generated raw artifacts.

### `failures.json`
If any structured failures occurred during the execution, they must be recorded here.

## Version 3 decisions

See [evaluation trust](evaluation-trust.md) for the authoritative current admission contract. New decisions are per model; a pooled mean cannot hide a failing model. Complete failed comparisons retain their evidence. Adapter invocation identity is explicitly configuration-only unless `implementation.files` pins declared local files. Pins do not cover undeclared dependencies or authenticate execution. Baseline JSON records now resolve run paths relative to the record.
