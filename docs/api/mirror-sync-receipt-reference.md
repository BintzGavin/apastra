---
title: "Mirror Sync Receipt"
description: "Schema for mirror sync receipts."
audience: "developers | platform-teams | agents | all"
last_verified: "2026-03-22"
source_files:
  - "promptops/schemas/mirror-sync-receipt.schema.json"
---

# Mirror Sync Receipt

Schema for mirror sync receipts.

## Properties

### `receipt_id`

- **Type:** `string`
- **Requirement:** Required
- **Description:** Unique identifier for the sync receipt.

### `mirror_id`

- **Type:** `string`
- **Requirement:** Required
- **Description:** The ID of the mirror.

### `synced_digests`

- **Type:** `array`
- **Requirement:** Required
- **Description:** Array of SHA-256 digests that were synced.
- **Items Type:** `string`

### `timestamp`

- **Type:** `string`
- **Requirement:** Required
- **Description:** The timestamp of the sync.

### `status`

- **Type:** `string`
- **Requirement:** Required
- **Description:** The status of the sync operation.
