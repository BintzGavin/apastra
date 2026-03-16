---
title: "Takedown Record Reference"
description: "Schema for takedown records."
audience: "developers | platform-teams | agents | all"
last_verified: "2026-03-11"
source_files:
  - "promptops/schemas/takedown-record.schema.json"
---

# Takedown Record Reference

Schema for takedown records.

## Properties

## `takedown_id`

- **Type:** string
- **Requirement:** Required
- **Description:** Unique identifier for the takedown record.

## `package_digest`

- **Type:** string
- **Requirement:** Required
- **Description:** The SHA-256 digest of the taken down package.

## `timestamp`

- **Type:** string
- **Requirement:** Required
- **Description:** The timestamp of the takedown.

## `reason`

- **Type:** string
- **Requirement:** Required
- **Description:** The reason for the takedown.

## `policy_violation_type`

- **Type:** string
- **Requirement:** Required
- **Description:** The type of policy violation.
