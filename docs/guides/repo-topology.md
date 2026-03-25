---
title: "Repo Topology"
description: "Understanding supported repository topologies"
audience: "developers | platform-teams | agents"
last_verified: "2026-03-25"
source_files:
  - "README.md"
---

# Repo Topology

The PromptOps system supports multiple repository topologies, each tailored to different team sizes and architectural needs, without changing the conceptual model or consumption contract.

## Supported Topologies

### Same-Repo

In a Same-Repo setup, the prompts reside in the same repository as the application that consumes them, typically organized under the `promptops/` directory.

- **Strengths:** Simplest adoption, allowing developers to manage prompts and the consuming application in a single PR.
- **Costs:** Limits cross-repo reuse, and the prompt lifecycle is tightly coupled to the application's release cadence.
- **Best Use Case:** Single-product teams or organizations starting out with structured prompt management.

### Separate Prompt Repo

The Separate Prompt Repo topology moves prompts into a dedicated repository. Consuming applications define their dependencies using Git ref pins, OCI artifacts, or package managers (e.g., npm/PyPI) in their `consumption.yaml` manifest.

- **Strengths:** Decouples prompt ownership and release lifecycles from any single application. Enables clear boundaries and broad reuse across multiple products.
- **Costs:** Requires managing a separate dependency update workflow. Teams must coordinate across repositories when modifying both prompts and applications.
- **Best Use Case:** Platform teams managing a central prompt library, or organizations where many applications share common prompts.

### Local-Linked Development

Local-Linked Development is a hybrid approach combining the benefits of a Separate Prompt Repo with the ergonomics of Same-Repo development. Consuming applications define a `local_override` mapping in their `consumption.yaml` manifest.

- **Strengths:** Enables rapid, local iteration without publishing intermediate artifacts to an upstream registry for every change. This mirrors a traditional "local link" or "workspace" dependency model.
- **Costs:** Requires standardizing the override paths and mechanisms to prevent "works on my machine" inconsistencies across developer environments.
- **Best Use Case:** Teams utilizing a Separate Prompt Repo that require frequent, simultaneous co-development of both the prompt and the consuming application.

## Appending Artifacts

Regardless of the chosen topology, PromptOps generates append-friendly, immutable artifacts (e.g., run records, regression reports, and promotion records). These generated files should be pushed to an independent "artifacts" branch to isolate derived records from the source-of-truth branch and prevent Git repository bloat.
