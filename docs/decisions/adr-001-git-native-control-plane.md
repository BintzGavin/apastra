---
title: "ADR 001: Git-Native Control Plane"
description: "Architecture decision record for using GitHub as the canonical control plane for PromptOps"
audience: "developers | platform-teams | agents"
last_verified: "2026-03-25"
source_files:
  - "README.md"
---

# ADR 001: Git-Native Control Plane

## Status

Accepted

## Context

The ecosystem for prompt evaluation and lifecycle management is largely fragmented into external prompt registries, CI-centric runners, and observability-first frameworks. Shifting the source of truth to a platform separate from the app's codebase breaks established developer workflows involving PRs, commits, required status checks, and peer review. Forcing users to adopt an external registry makes audit trails and deployment lineage much harder to enforce.

## Decision

We will use GitHub (and Git primitives) as the primary control plane for PromptOps.
- Prompt definitions, suite specs, regression policies, and delivery targets will be managed as versioned files inside a Git repository.
- Changes to prompts will be gated using standard PR reviews, CODEOWNERS, and branch protection rules requiring status checks.
- Artifacts and releases will be anchored by Git commit SHAs, tags, or content digests.
- Downstream consumption will rely on git ref pinning or local overrides by default, falling back to governed releases (OCI/GitHub Release assets) when needed.

## Consequences

- **Positive:** Leverages existing developer ergonomics and CI/CD tools without forcing adoption of an external SaaS platform.
- **Positive:** Enables robust audit trails and rollback safety.
- **Negative:** Requires storing append-only artifacts (like run artifacts and regression reports) to a designated "artifacts branch" or external system to avoid repo bloat and bypass ephemeral CI log retention limits.
- **Negative:** Non-technical domain experts may find raw Git workflows challenging unless custom UIs or bots are layered on top of the repo.
