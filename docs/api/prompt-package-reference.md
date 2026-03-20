---
title: "Prompt Package Manifest Reference"
description: "Immutable bundle of prompt specs with a manifest and content digest."
audience: "developers | platform-teams | agents | all"
last_verified: "2026-03-20"
source_files:
  - "promptops/schemas/prompt-package.schema.json"
---

# Prompt Package Manifest Reference

Immutable bundle of prompt specs with a manifest and content digest.

## Properties

## `id`

- **Type:** string
- **Requirement:** Required
- **Description:** Stable identifier for the package.

## `digest`

- **Type:** string
- **Requirement:** Required
- **Description:** Content digest of the package, computed over canonicalized JSON using SHA-256.

## `specs`

- **Type:** array of string
- **Requirement:** Required
- **Description:** Array of included prompt spec IDs/digests.

## `version`

- **Type:** string
- **Requirement:** Optional
- **Description:** Optional semantic version for the package.

## `metadata`

- **Type:** object
- **Requirement:** Optional
- **Description:** Optional metadata (e.g., provenance, author).

