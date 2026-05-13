---
title: "Architecture Overview"
description: "High-level overview of the PromptOps architecture"
audience: "developers | platform-teams | agents | all"
last_verified: "2026-05-13"
source_files:
  - "README.md"
---

# Architecture Overview

The PromptOps system is built around file-based durable state as the source of truth. Computation is stateless and replaceable, enabling teams to govern prompts like standard software assets via Git-based workflows.

## Core Tenets

1. **Git as the Control Plane:** All prompt specifications, test suites, and regression policies reside in Git. Governance (PRs, required status checks, protected branches) relies on GitHub's native tools.
2. **Bring-Your-Own Harness:** The system imposes a strict, minimal interface on execution: a run request acts as an immutable work order, and the compute layer (often the user's IDE agent) emits a durable run artifact directory. This decoupling prevents vendor lock-in and accommodates varying runtimes.
3. **Stateless Compute:** Tools that evaluate prompts against datasets generate structured output records but maintain no hidden, internal state. They read source state and emit append-friendly derived state.
4. **Content Digest Identity:** All core evaluation components (prompts, datasets, evaluators) are identified and pinned using canonical content digests. This ensures absolute reproducibility when evaluating regressions and deploying updates.
5. **Trace Evidence:** Agent hooks expose tool calls, validation feedback, retries, and stopping conditions while the agent works. Useful trace evidence is stored as sanitized run artifacts or artifact references, not as hidden platform state.

## Structural Domains

The architecture operates across five active functional domains:

### CONTRACTS
The foundation of the system. This domain manages the JSON schema specifications (`prompt-spec.schema.json`, `suite.schema.json`, `run-request.schema.json`) that govern all structured communication and validation throughout the architecture.

### RUNTIME
Responsible for rendering and retrieving target prompts. The Python-based resolver chain dictates the precedence of loading prompt packages via local overrides, workspace paths, Git refs, or packaged artifacts using a `consumption-manifest`.

### EVALUATION
Owns the lifecycle of benchmark execution and baseline tracking. Operating under the Bring-Your-Own (BYO) harness contract, this domain translates run requests into verifiable run artifacts, generating scorecards and metrics.

### TRACE
Connects agent runtime behavior to eval evidence. Codex and Claude Code hooks surface prompt-submit, tool-use, validation, and stop events; the `apastra-trace` skill turns relevant trace evidence into cases, assertions, and artifact references.

### GOVERNANCE
Enforces quality and compliance. This domain establishes required status checks driven by regression reports, automates promotion records, and dictates the sync mechanics to downstream delivery targets.
