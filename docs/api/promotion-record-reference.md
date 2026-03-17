---
title: "Promotion Record Reference"
description: "API reference for promotion-record schema"
audience: "all"
last_verified: "2026-03-15"
source_files:
  - "promptops/schemas/promotion-record.schema.json"
---

# Promotion Record Reference

Schema for append-only binding records.

## Properties

### `version`
- **Type**: string
- **Presence**: **Required**
- **Description**: The approved version

### `channel`
- **Type**: string
- **Presence**: **Required**
- **Description**: The channel to bind to, e.g., 'prod'

### `digest`
- **Type**: string
- **Presence**: **Required**
- **Description**: The content digest of the version

### `evidence`
- **Type**: object
- **Presence**: *Optional*
- **Description**: Links to evidence

### `evidence.run_id`
- **Type**: string
- **Presence**: *Optional*
- **Description**: Release candidate run ID

### `timestamp`
- **Type**: string
- **Presence**: *Optional*
- **Description**: Timestamp of the promotion
