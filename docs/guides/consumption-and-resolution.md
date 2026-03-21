---
title: "Consumption and Resolution"
description: "Understanding prompt consumption and the resolver chain"
audience: "developers | platform-teams | agents"
last_verified: "2026-03-21"
source_files:
  - "README.md"
---

# Consumption and Resolution

The PromptOps system leverages a Git-first resolution model that allows teams to iterate rapidly without enforcing mandatory packaging for every minor edit. A robust resolution chain handles the transition from local development to production distribution.

## Consumption Manifests

The `consumption.yaml` manifest is the app-side file declaring the exact prompt dependencies required by a downstream application. It maps local prompt IDs to their corresponding versions, utilizing standard Git mechanisms (tags, commit SHAs) or semantic versions.

## Resolution Precedence

When an application queries the `promptops` resolver to load a prompt, the system relies on a predefined hierarchy to fetch the correct asset. This ensures seamless development across local environments, feature branches, and governed release artifacts.

The resolution chain follows this strict order:

1. **Local Override**: Local filesystem path resolution. This allows developers to iterate quickly by referencing their working copy of the prompt repository without committing or publishing.
2. **Workspace Path**: For same-repo configurations, the resolver searches the `promptops/` workspace directory.
3. **Git Ref**: Resolves dependencies using a Git commit SHA or tag. This is the default mechanism for separate-repo consumption during early adoption and CI/CD pipelines.
4. **Packaged Artifact**: Fetches a released artifact (e.g., GitHub Release asset, OCI digest, npm/PyPI registry wrapper) when rigorous distribution guarantees and immutability are required.

## The Git-First Posture

The core design philosophy is that packaging and publishing should be optional for daily development.

Developers can edit prompt files and test them using local overrides or workspace paths without generating an OCI image or npm package. When a change is merged, CI can trigger suites based on the Git ref. Packaging is reserved for formal, governed releases to downstream environments.
