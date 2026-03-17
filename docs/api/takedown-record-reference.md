---
title: "Takedown Record Reference"
description: "API reference for takedown-record schema"
audience: "all"
last_verified: "2026-03-15"
source_files:
  - "promptops/schemas/takedown-record.schema.json"
---

# Takedown Record Reference

Schema for takedown records.

## Properties

### `takedown_id`
- **Type**: string
- **Presence**: **Required**
- **Description**: Unique identifier for the takedown record.

### `package_digest`
- **Type**: string
- **Presence**: **Required**
- **Description**: The SHA-256 digest of the taken down package.

### `timestamp`
- **Type**: string
- **Presence**: **Required**
- **Description**: The timestamp of the takedown.

### `reason`
- **Type**: string
- **Presence**: **Required**
- **Description**: The reason for the takedown.

### `policy_violation_type`
- **Type**: string
- **Presence**: **Required**
- **Description**: The type of policy violation.
