---
title: "Moderation Escalation Record"
description: "Schema for a moderation escalation record."
audience: "developers | platform-teams | agents | all"
last_verified: "2026-03-22"
source_files:
  - "promptops/schemas/moderation-escalation-record.schema.json"
---

# Moderation Escalation Record

Schema for a moderation escalation record.

## Properties

### `escalation_id`

- **Type:** `string`
- **Requirement:** Required
- **Description:** Unique identifier for the escalation.

### `submission_id`

- **Type:** `string`
- **Requirement:** Required
- **Description:** Unique identifier for the submission.

### `escalated_by`

- **Type:** `string`
- **Requirement:** Required
- **Description:** User who escalated the content.

### `reason`

- **Type:** `string`
- **Requirement:** Required
- **Description:** Reason for the escalation.

### `timestamp`

- **Type:** `string`
- **Requirement:** Required
- **Description:** Timestamp of the escalation.

### `status`

- **Type:** `string`
- **Requirement:** Required
- **Description:** Status of the escalation.
- **Allowed Values:** `pending`, `reviewed`, `dismissed`

### `reviewer_id`

- **Type:** `string`
- **Requirement:** Optional
- **Description:** User who reviewed the escalation.

### `notes`

- **Type:** `string`
- **Requirement:** Optional
- **Description:** Additional notes.
