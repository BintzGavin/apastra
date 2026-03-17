---
title: "Moderation Decision Record Reference"
description: "API reference for moderation-decision-record schema"
audience: "all"
last_verified: "2026-03-15"
source_files:
  - "promptops/schemas/moderation-decision-record.schema.json"
---

# Moderation Decision Record Reference

Schema for moderation decision records.

## Properties

### `decision_id`
- **Type**: string
- **Presence**: **Required**
- **Description**: Unique identifier for the moderation decision.

### `submission_id`
- **Type**: string
- **Presence**: *Optional*
- **Description**: The ID of the submission this decision applies to.

### `package_digest`
- **Type**: string
- **Presence**: *Optional*
- **Description**: The SHA-256 digest of the package this decision applies to.

### `decision`
- **Type**: enum (`approved`, `rejected`, `flagged`)
- **Presence**: **Required**
- **Description**: The moderation decision made.

### `moderator_id`
- **Type**: string
- **Presence**: **Required**
- **Description**: The ID of the moderator who made the decision.

### `timestamp`
- **Type**: string
- **Presence**: **Required**
- **Description**: The timestamp of the decision.

### `reason`
- **Type**: string
- **Presence**: **Required**
- **Description**: The reason for the decision.
