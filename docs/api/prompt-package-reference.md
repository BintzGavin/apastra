---
title: "Prompt Package Reference"
description: "API reference for prompt-package schema"
audience: "all"
last_verified: "2026-03-15"
source_files:
  - "promptops/schemas/prompt-package.schema.json"
---

# Prompt Package Reference

Immutable bundle of prompt specs with a manifest and content digest.

## Properties

### `id`
- **Type**: string
- **Presence**: **Required**
- **Description**: Stable identifier for the package.

### `digest`
- **Type**: string
- **Presence**: **Required**
- **Description**: Content digest of the package, computed over canonicalized JSON using SHA-256.

### `specs`
- **Type**: array of string
- **Presence**: **Required**
- **Description**: Array of included prompt spec IDs/digests.

### `version`
- **Type**: string
- **Presence**: *Optional*
- **Description**: Optional semantic version for the package.

### `metadata`
- **Type**: object
- **Presence**: *Optional*
- **Description**: Optional metadata (e.g., provenance, author).
