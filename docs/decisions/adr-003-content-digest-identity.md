---
title: "ADR 003: Content Digest Identity"
description: "Architecture decision record for establishing content digests as the core identity for packages"
audience: "developers | platform-teams | agents"
last_verified: "2026-03-22"
source_files:
  - "README.md"
---

# ADR 003: Content Digest Identity

## Status

Accepted

## Context

When versioning code, tags and SHAs naturally define identity. However, when evaluating and promoting dynamic assets like datasets, prompts, and suites, reproducibility is paramount. A semantic version or branch name is mutable, and simple SHA pinning can change without modifying the core logical asset due to formatting noise or whitespace.

## Decision

Content digests are the canonical identity mechanism for packages (prompts, datasets, evaluators). These identities guarantee reproducibility ("what exactly ran" and "what exactly shipped"). They are the primary key linking runs, baselines, and promotion records. SemVer will be supported only as an optional layer when declaring a public interface.

## Consequences

- **Positive:** Guarantees reproducibility and strict mapping between source and derived evaluation artifacts.
- **Positive:** Protects against unintentional mutations or supply chain tampering when fetching artifacts.
- **Negative:** Requires rigorous normalization and deterministic canonicalization logic across different data formats (e.g., JSON, YAML) before hashing.
- **Negative:** Small stylistic changes alter the digest unless pre-filtered, which could result in unnecessary digest churn if the canonicalization process is weak.
