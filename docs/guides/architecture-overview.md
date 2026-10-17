---
title: "Architecture Overview"
description: "The implemented evidence and decision boundary"
audience: "developers | platform-teams | agents"
last_verified: "2026-10-17"
source_files:
  - "promptops/runtime/runner.py"
  - "promptops/runtime/evidence.py"
  - "promptops/runtime/gate.py"
  - "promptops/runtime/ci_workflow.py"
---

# Architecture Overview

Apastra is a file-based evaluation evidence verifier. The execution engine is replaceable; the admission rules are explicit. Its useful unit is a retained run that another checkout can inspect and re-evaluate under the same policy.

```mermaid
flowchart LR
  A[Versioned inputs] --> B[Resolve immutable request]
  B --> C[Reviewed external harness]
  C --> D[Outputs and per-trial scores]
  D --> E[Validate coverage, identity, arithmetic]
  E --> F[Apply policy to each model]
  F --> G[Baseline or revision-bound CI gate]
```

## Boundaries

| Component | Responsibility | Does not prove |
| --- | --- | --- |
| Resolver and digest | Snapshot prompt, cases, evaluators, suite and sampling | Repeatability of model output |
| Adapter | Execute requested targets and score actual outputs | Producer honesty merely by emitting files |
| Evidence validator | Exact coverage, finite scores, matching means, file integrity | Correctness of arbitrary evaluator code |
| Decision layer | Thresholds and regression rules for every model | Statistical significance or general model quality |
| Baseline record | Immutable named reference and run digest | That evidence will remain available elsewhere |
| CI launcher | Bind gate to checkout SHA and current inputs; fail on missing configuration/evidence | Branch protection or trusted producer configuration on GitHub |

`runtime/evidence.py` is shared by execution and admission. `runner.py` owns the subprocess boundary. `gate.py` owns baseline and regression decisions. `ci_workflow.py` adapts that contract to GitHub Actions. Installation packages these modules without copying run data.

Adapter identity distinguishes configuration-only bindings from explicitly pinned implementation files. Pinned files are checked before and after execution and on admission. This is a declared file set, not a dependency closure or an authenticated attestation. Dependencies, external services, model aliases and provider behavior can change.

## Supported surface

The executable core comprises suite/quick evaluation, comparisons, evidence admission, baselines, regression policies, asset validation, digests and revision-bound CI. MCP exposes a workspace-scoped subset. Skills help author cases and configure these commands. Hooks and the opt-in provider request logger are auxiliary local tools; their receipts are not evaluation passes.

Schemas for delivery, canaries, registry/moderation, signatures, promotion and observability are design records. A schema's existence is not implementation evidence. Delivery and canary workflow entry points fail explicitly until real integrations exist. Do not require users to configure speculative domains to run an eval.

See [evaluation trust](evaluation-trust.md) for the exact admission contract and [product direction](../vision.md) for the remaining hypothesis.
