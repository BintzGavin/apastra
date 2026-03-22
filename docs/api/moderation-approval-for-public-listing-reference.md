---
title: "Moderation Approval for Public Listing"
description: "Schema for moderation approval for public listing records."
audience: "developers | platform-teams | agents | all"
last_verified: "2026-03-22"
source_files:
  - "promptops/schemas/moderation-approval-for-public-listing.schema.json"
---

# Moderation Approval for Public Listing

Schema for moderation approval for public listing records.

## Properties

### `approval_id`

- **Type:** `string`
- **Requirement:** Required
- **Description:** Unique identifier for the moderation approval.

### `package_digest`

- **Type:** `string`
- **Requirement:** Required
- **Description:** The SHA-256 digest of the package being approved.

### `approver_id`

- **Type:** `string`
- **Requirement:** Required
- **Description:** The ID of the moderator who approved the listing.

### `timestamp`

- **Type:** `string`
- **Requirement:** Required
- **Description:** The timestamp of the approval.

### `listing_tier`

- **Type:** `string`
- **Requirement:** Required
- **Description:** The tier of the public listing.
