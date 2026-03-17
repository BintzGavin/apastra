---
title: "Provider Artifact Reference"
description: "API reference for provider-artifact schema"
audience: "all"
last_verified: "2026-03-15"
source_files:
  - "promptops/schemas/provider-artifact.schema.json"
---

# Provider Artifact Reference

A distribution wrapper around a prompt package (git ref, release asset, OCI artifact, npm/PyPI wrapper).

## Properties

### `id`
- **Type**: string
- **Presence**: **Required**
- **Description**: Stable identifier for the provider artifact.

### `type`
- **Type**: enum (`git_ref`, `release_asset`, `oci_artifact`, `npm_wrapper`, `pypi_wrapper`)
- **Presence**: **Required**
- **Description**: The distribution type of the wrapper.

### `reference`
- **Type**: string
- **Presence**: **Required**
- **Description**: The URI, ref, or tag of the wrapper.

### `package_digest`
- **Type**: string
- **Presence**: **Required**
- **Description**: Content digest of the underlying prompt package.

### `metadata`
- **Type**: object
- **Presence**: *Optional*
- **Description**: Arbitrary key-value pairs for registry-specific data, provenance, or signatures.
