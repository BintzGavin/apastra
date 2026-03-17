---
title: "Mirror Sync Receipt Reference"
description: "API reference for mirror-sync-receipt schema"
audience: "all"
last_verified: "2026-03-15"
source_files:
  - "promptops/schemas/mirror-sync-receipt.schema.json"
---

# Mirror Sync Receipt Reference

Schema for mirror sync receipts.

## Properties

### `receipt_id`
- **Type**: string
- **Presence**: **Required**
- **Description**: Unique identifier for the sync receipt.

### `mirror_id`
- **Type**: string
- **Presence**: **Required**
- **Description**: The ID of the mirror.

### `synced_digests`
- **Type**: array of string
- **Presence**: **Required**
- **Description**: Array of SHA-256 digests that were synced.

### `timestamp`
- **Type**: string
- **Presence**: **Required**
- **Description**: The timestamp of the sync.

### `status`
- **Type**: string
- **Presence**: **Required**
- **Description**: The status of the sync operation.
