---
title: "Provider Artifact Manifest"
description: "A distribution wrapper around a prompt package (git ref, release asset, OCI artifact, npm/PyPI wrapper)."
audience: "developers | platform-teams | agents | all"
last_verified: "2026-03-22"
source_files:
  - "promptops/schemas/provider-artifact.schema.json"
---

# Provider Artifact Manifest

A distribution wrapper around a prompt package (git ref, release asset, OCI artifact, npm/PyPI wrapper).

## Properties

### `id`

- **Type:** `string`
- **Requirement:** Required
- **Description:** Stable identifier for the provider artifact.

### `type`

- **Type:** `string`
- **Requirement:** Required
- **Description:** The distribution type of the wrapper.
- **Allowed Values:** `git_ref`, `release_asset`, `oci_artifact`, `npm_wrapper`, `pypi_wrapper`

### `reference`

- **Type:** `string`
- **Requirement:** Required
- **Description:** The URI, ref, or tag of the wrapper.

### `package_digest`

- **Type:** `string`
- **Requirement:** Required
- **Description:** Content digest of the underlying prompt package.

### `metadata`

- **Type:** `object`
- **Requirement:** Optional
- **Description:** Arbitrary key-value pairs for registry-specific data, provenance, or signatures.
