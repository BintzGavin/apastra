---
title: "Promotion and Delivery"
description: "Understanding prompt promotion and downstream delivery"
audience: "developers | platform-teams | agents"
last_verified: "2026-03-23"
source_files:
  - "README.md"
---

# Promotion and Delivery

The PromptOps system leverages a governed release workflow that transitions approved prompt packages from their evaluated Git state to downstream delivery targets.

## The Promotion Workflow

Promotion is an explicit state transition managed within the repository's control plane. Floating prompts (e.g., "latest") are strongly discouraged; production systems must pin specific content digests to guarantee predictability and enable auditable rollbacks.

1. **Evaluation and Approval**: A candidate PR passes all required CI checks, generating a regression report.
2. **Merge and Release**: The PR is merged, and optionally, a release candidate run generates a new Git tag and immutable GitHub Release asset.
3. **Promotion Record Creation**: An append-only promotion record binds the approved prompt package (by digest) to a specific delivery channel (e.g., "prod").
4. **Delivery Target Synchronization**: A declarative delivery worker reads the promotion record and executes the sync logic to push the asset downstream.

## Delivery Targets

The system abstracts the delivery mechanism. Because PromptOps doesn't enforce a specific SaaS platform or distribution network, delivery targets are declarative configuration files that dictate the destination of the promoted asset.

Examples of typical delivery targets include:

- **Git-Native PR**: Opening a pull request against a downstream application repository to update its `consumption.yaml` manifest with the new pinned digest.
- **OCI Registry Sync**: Publishing a tagged OCI image digest to an internal enterprise registry.
- **Config Store Update**: Syncing the approved prompt definition to a distributed key-value store or edge cache accessed by runtime services.
- **Release Descriptor API**: Posting a signed manifest or release descriptor to a proprietary internal API.

## Rollback

A rollback in this model is simply a promotion to a prior, previously approved digest. It is managed identically to a forward promotion, leveraging the same verifiable promotion records and downstream delivery automation.
