---
title: "ADR 003: Content Digest Identity"
description: "Architecture decision record for establishing content digests as the core identity for packages"
audience: "developers | platform-teams | agents"
last_verified: "2026-10-17"
source_files:
  - "README.md"
---

# ADR 003: Content Digest Identity

## Status

Accepted

## Context

When versioning code, tags and SHAs naturally define identity. However, when evaluating and promoting dynamic assets like datasets, prompts, and suites, reproducibility is paramount. A semantic version or branch name is mutable, and simple SHA pinning can change without modifying the core logical asset due to formatting noise or whitespace.

## Decision

Content digests are the canonical identity mechanism for packages (prompts, datasets, evaluators). These identities bind records to specific input content. They do not guarantee repeatable model output or authenticate what a producer executed. They are the primary key linking runs, baselines, and promotion records. SemVer will be supported only as an optional layer when declaring a public interface.

## Consequences

- **Positive:** Detects changes between retained input snapshots and current source assets.
- **Positive:** Detects changed bytes when an independently trusted expected digest is available; authenticity requires a separate trust mechanism.
- **Negative:** Requires rigorous normalization and deterministic canonicalization logic across different data formats (e.g., JSON, YAML) before hashing.
- **Negative:** Structured-asset canonicalization ignores formatting-only changes; raw implementation-file and artifact digests intentionally cover every byte.
