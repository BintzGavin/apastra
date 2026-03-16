---
title: "Mirror Sync Receipt Reference"
description: "Schema for mirror sync receipts."
audience: "developers | platform-teams | agents | all"
last_verified: "2026-03-11"
source_files:
  - "promptops/schemas/mirror-sync-receipt.schema.json"
---

# Mirror Sync Receipt Reference

Schema for mirror sync receipts.

## Properties

## `receipt_id`

- **Type:** string
- **Requirement:** Required
- **Description:** Unique identifier for the sync receipt.

## `mirror_id`

- **Type:** string
- **Requirement:** Required
- **Description:** The ID of the mirror.

## `synced_digests`

- **Type:** array of string
- **Requirement:** Required
- **Description:** Array of SHA-256 digests that were synced.

## `timestamp`

- **Type:** string
- **Requirement:** Required
- **Description:** The timestamp of the sync.

## `status`

- **Type:** string
- **Requirement:** Required
- **Description:** The status of the sync operation.
