---
title: "Moderation Decision Record Reference"
description: "Schema for moderation decision records."
audience: "developers | platform-teams | agents | all"
last_verified: "2026-03-20"
source_files:
  - "promptops/schemas/moderation-decision-record.schema.json"
---

# Moderation Decision Record Reference

Schema for moderation decision records.

## Properties

## `decision_id`

- **Type:** string
- **Requirement:** Required
- **Description:** Unique identifier for the moderation decision.

## `submission_id`

- **Type:** string
- **Requirement:** Optional
- **Description:** The ID of the submission this decision applies to.

## `package_digest`

- **Type:** string
- **Requirement:** Optional
- **Description:** The SHA-256 digest of the package this decision applies to.

## `decision`

- **Type:** string
- **Requirement:** Required
- **Description:** The moderation decision made.
- **Allowed Values:** approved, rejected, flagged

## `moderator_id`

- **Type:** string
- **Requirement:** Required
- **Description:** The ID of the moderator who made the decision.

## `timestamp`

- **Type:** string
- **Requirement:** Required
- **Description:** The timestamp of the decision.

## `reason`

- **Type:** string
- **Requirement:** Required
- **Description:** The reason for the decision.

