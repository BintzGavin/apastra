---
title: "Deprecation Record"
description: "Schema for deprecation records."
audience: "developers | platform-teams | agents | all"
last_verified: "2026-03-22"
source_files:
  - "promptops/schemas/deprecation-record.schema.json"
---

# Deprecation Record

Schema for deprecation records.

## Properties

### `deprecation_id`

- **Type:** `string`
- **Requirement:** Required
- **Description:** Unique identifier for the deprecation record.

### `package_digest`

- **Type:** `string`
- **Requirement:** Optional
- **Description:** The SHA-256 digest of the deprecated package.

### `reference`

- **Type:** `string`
- **Requirement:** Optional
- **Description:** The reference of the deprecated package.

### `timestamp`

- **Type:** `string`
- **Requirement:** Required
- **Description:** The timestamp of the deprecation.

### `reason`

- **Type:** `string`
- **Requirement:** Required
- **Description:** The reason for the deprecation.

### `replacement_ref`

- **Type:** `string`
- **Requirement:** Optional
- **Description:** The reference to the suggested replacement.
