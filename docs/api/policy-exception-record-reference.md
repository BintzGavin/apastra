---
title: "Policy Exception Record"
description: "Schema for policy exception records"
audience: "developers | platform-teams | agents | all"
last_verified: "2026-03-22"
source_files:
  - "promptops/schemas/policy-exception-record.schema.json"
---

# Policy Exception Record

Schema for policy exception records

## Properties

### `exception_id`

- **Type:** `string`
- **Requirement:** Required
- **Description:** Unique identifier for the exception

### `policy_id`

- **Type:** `string`
- **Requirement:** Required
- **Description:** The policy being bypassed

### `target_digest`

- **Type:** `string`
- **Requirement:** Required
- **Description:** The digest of the package/artifact receiving the exception

### `approver_id`

- **Type:** `string`
- **Requirement:** Required
- **Description:** The person granting the exception

### `reason`

- **Type:** `string`
- **Requirement:** Required
- **Description:** Explanation for the exception

### `timestamp`

- **Type:** `string`
- **Requirement:** Required
- **Description:** Timestamp when the exception was granted
