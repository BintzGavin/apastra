---
title: "Deprecation Record Reference"
description: "API reference for deprecation-record schema"
audience: "all"
last_verified: "2026-03-15"
source_files:
  - "promptops/schemas/deprecation-record.schema.json"
---

# Deprecation Record Reference

Schema for deprecation records.

## Properties

### `deprecation_id`
- **Type**: string
- **Presence**: **Required**
- **Description**: Unique identifier for the deprecation record.

### `package_digest`
- **Type**: string
- **Presence**: *Optional*
- **Description**: The SHA-256 digest of the deprecated package.

### `reference`
- **Type**: string
- **Presence**: *Optional*
- **Description**: The reference of the deprecated package.

### `timestamp`
- **Type**: string
- **Presence**: **Required**
- **Description**: The timestamp of the deprecation.

### `reason`
- **Type**: string
- **Presence**: **Required**
- **Description**: The reason for the deprecation.

### `replacement_ref`
- **Type**: string
- **Presence**: *Optional*
- **Description**: The reference to the suggested replacement.
