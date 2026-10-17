---
title: "ADR 002: Bring-Your-Own Harnesses"
description: "Architecture decision record for adopting a minimal BYO harness contract"
audience: "developers | platform-teams | agents"
last_verified: "2026-10-17"
source_files:
  - "README.md"
---

# ADR 002: Bring-Your-Own Harnesses

## Status

Accepted

## Context

Many PromptOps frameworks couple their ecosystem deeply to their specific execution environment, languages, or runtime assumptions. When teams are locked into one harness or evaluator framework, migrating across the fast-moving landscape of model providers and emerging LLM frameworks requires rewriting source-of-truth prompt assets and suite definitions.

## Decision

We will mandate a "Bring-Your-Own" (BYO) harness contract. The system defines a minimal interface ("run request in, run artifact out"). Any compute tool—whether a Python script, an internal scheduler, or an existing framework (like promptfoo or OpenAI Evals)—can serve as the harness, provided it adheres to the contract. Apastra resolves and fingerprints the inputs. The harness executes the requested models and evaluators and emits complete per-trial evidence. Apastra independently validates that evidence and applies policy.

## Consequences

- **Positive:** No lock-in to any specific evaluation or compute framework.
- **Positive:** Accommodates a vast range of environments (scripts, schedulers, notebooks).
- **Positive:** Harnesses can share the input contract; changing execution or evaluator semantics requires new evidence and may require a new baseline.
- **Negative:** Teams must provide or configure their own compute layer to perform actual prompt evaluation and emit properly formatted artifacts.
