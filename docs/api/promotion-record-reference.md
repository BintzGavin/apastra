---
title: "Promotion Record Specification"
description: "Schema for append-only binding records."
audience: "developers | platform-teams | agents | all"
last_verified: "2026-03-22"
source_files:
  - "promptops/schemas/promotion-record.schema.json"
---

# Promotion Record Specification

Schema for append-only binding records.

## Properties

### `version`

- **Type:** `string`
- **Requirement:** Required
- **Description:** The approved version

### `channel`

- **Type:** `string`
- **Requirement:** Required
- **Description:** The channel to bind to, e.g., 'prod'

### `digest`

- **Type:** `string`
- **Requirement:** Required
- **Description:** The content digest of the version

### `evidence`

- **Type:** `object`
- **Requirement:** Optional
- **Description:** Links to evidence

### `timestamp`

- **Type:** `string`
- **Requirement:** Optional
- **Description:** Timestamp of the promotion
