---
title: "Promotion Record Specification Reference"
description: "Schema for append-only binding records."
audience: "developers | platform-teams | agents | all"
last_verified: "2026-03-11"
source_files:
  - "promptops/schemas/promotion-record.schema.json"
---

# Promotion Record Specification Reference

Schema for append-only binding records.

## Properties

## `version`

- **Type:** string
- **Requirement:** Required
- **Description:** The approved version

## `channel`

- **Type:** string
- **Requirement:** Required
- **Description:** The channel to bind to, e.g., 'prod'

## `digest`

- **Type:** string
- **Requirement:** Required
- **Description:** The content digest of the version

## `evidence`

- **Type:** object
- **Requirement:** Optional
- **Description:** Links to evidence

### `run_id`

- **Type:** string
- **Requirement:** Optional
- **Description:** Release candidate run ID

## `timestamp`

- **Type:** string
- **Requirement:** Optional
- **Description:** Timestamp of the promotion
