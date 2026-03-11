---
title: "Harness Contract"
description: "Understanding the minimal BYO harness contract"
audience: "developers | platform-teams | agents"
last_verified: "2026-03-11"
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

1. **Resolve Revisions:** Identify and bind the revision reference to a concrete, reproducible prompt package digest.
2. **Execute Suites:** Process the benchmark suite across the specified datasets and model matrix.
3. **Apply Evaluators:** Evaluate the outputs and produce consistent metrics.
4. **Emit Run Artifacts:** Populate the structured run artifact directory.
5. **Attach Raw Traces:** Attach references (URIs) and digests to raw text, logs, and traces.
6. **Record Environment Metadata:** Capture data required to reproduce the run (model IDs, sampling configurations, harness version).

## Required Outputs

The harness must generate the following standard structures inside the artifact directory:

### `run_manifest.json`
A comprehensive metadata record. It must contain the resolved digests, timestamps, harness version, model IDs, sampling configs, environment data, and the overall status.

### `scorecard.json`
The normalized evaluation results. This file holds the metrics, metric definitions, metric versioning, and trial variance data.

### `cases.jsonl`
A detailed per-case record file. It must include stable case IDs, per-trial outputs, evaluation outputs, and pointers to raw artifacts (traces, text).

### `artifact_refs.json`
A manifest of URIs and corresponding digests referencing the generated raw artifacts.

### `failures.json`
If any structured failures occurred during the execution, they must be recorded here.
