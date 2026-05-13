---
title: "Getting Started"
description: "A quick guide to getting started with Apastra"
audience: "developers | platform-teams | agents | all"
last_verified: "2026-05-13"
source_files:
  - "README.md"
---

# Getting Started

Apastra treats prompts as versioned software assets with a declared interface, and evaluation evidence as portable, reproducible, and gateable through GitHub's native tools.

This guide provides a conceptual overview of the key concepts and workflows you'll interact with.

## Key Concepts

### Prompt Specs
The source-of-truth definition for your prompts. They define stable IDs, variable schemas, output contracts, and metadata.

### Benchmark Suites
Suites bind datasets, evaluators, and a model matrix into an executable benchmark. This is what your CI runs to detect regressions.

### Datasets and Evaluators
Datasets provide versioned evaluation cases (typically JSONL format), while Evaluators define the scoring mechanism (e.g., deterministic checks, schema validation, rubric scoring).

### The Harness Contract
Apastra is compute-agnostic. It implements a strict "run request in, run artifact out" contract. Your execution environment (often your IDE agent, but also a Python script, internal scheduler, or existing tool like OpenAI Evals) reads the run request and emits standardized artifacts.

### Agent Traces
Codex and Claude Code hooks can expose trace context while the agent works: prompt-submit events, tool calls, validation feedback, retries, and stopping conditions. Apastra treats useful traces as evidence. Store sanitized summaries in run artifacts or link larger/private traces through `artifact_refs.json`.

### The Resolver and Consumption
Apps consume prompts via a Git-first resolver. A `consumption.yaml` manifest defines the exact pins (tag, SHA, or semver tag) the application requires. The resolver supports a local override for fast, un-published iteration.

## The Developer Workflow

The default developer loop emphasizes local ergonomics:

1. **Edit Prompt Specs**: Modify your prompt definition files locally.
2. **Inspect Trace Evidence**: If a real agent failure motivated the change, use the trace evidence to define the behavior you want to lock down.
3. **Local Smoke Evaluation**: Run a quick local test suite using your agent or harness implementation.
4. **Open a PR**: Commit your changes and push them to a feature branch as you normally would.
5. **CI Triggers Suites**: The GitHub Actions runner executes full regression suites against your changes.
6. **Review Regression Report**: The results are generated and posted as a status check against your PR.
7. **Merge on Passing Policy**: If the regression policy is satisfied, your PR is eligible to merge.
8. **Optional Governed Release**: Release tags, immutable GitHub Releases, and promotion records are managed automatically post-merge.

## Repo Topologies

Apastra supports three main structures:

1. **Same-Repo:** Prompts and app source code live in the same repository under the `promptops/` directory. The simplest way to start.
2. **Separate Prompt Repo:** Prompts reside in a dedicated repository. Apps specify their dependencies via a Git ref pin or packaged artifact.
3. **Local-Linked Dev:** A hybrid approach using local overrides to develop prompts in a separate repository without needing to publish artifacts for every change.
