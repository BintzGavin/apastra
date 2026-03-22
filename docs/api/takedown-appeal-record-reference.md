---
title: "Takedown Appeal Record"
description: "A record used to formally process and track appeals to moderation takedowns."
audience: "developers | platform-teams | agents | all"
last_verified: "2026-03-22"
source_files:
  - "promptops/schemas/takedown-appeal-record.schema.json"
---

# Takedown Appeal Record

A record used to formally process and track appeals to moderation takedowns.

## Properties

### `appeal_id`

- **Type:** `string`
- **Requirement:** Required
- **Description:** Unique identifier for this takedown appeal.

### `takedown_record_id`

- **Type:** `string`
- **Requirement:** Required
- **Description:** Reference to the original takedown record being appealed.

### `appellant_id`

- **Type:** `string`
- **Requirement:** Required
- **Description:** Identifier of the user or entity filing the appeal.

### `reasoning`

- **Type:** `string`
- **Requirement:** Required
- **Description:** Text reasoning explaining why the takedown should be overturned.

### `status`

- **Type:** `string`
- **Requirement:** Required
- **Description:** Current status of the appeal.
- **Allowed Values:** `pending`, `approved`, `rejected`

### `evidence_links`

- **Type:** `array`
- **Requirement:** Optional
- **Description:** Optional array of links providing evidence to support the appeal.
- **Items Type:** `string`
