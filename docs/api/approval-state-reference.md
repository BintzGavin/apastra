---
title: "Approval State Reference"
description: "Schema for an Approval state record indicating human and machine review results."
audience: "developers | platform-teams | agents | all"
last_verified: "2026-03-21"
source_files:
  - "promptops/schemas/approval-state.schema.json"
---

# Approval State Reference

Schema for an Approval state record indicating human and machine review results.

## Properties

## `revision_ref`

- **Type:** `string`
- **Requirement:** Required
- **Description:** Target digest or ID of the revision or package.

## `checks_passed`

- **Type:** `boolean`
- **Requirement:** Required
- **Description:** Whether the required machine checks have passed.

## `human_review`

- **Type:** `object`
- **Requirement:** Required
- **Description:** Details of the manual human review.

## `decision`

- **Type:** `string`
- **Requirement:** Required
- **Description:** The final decision of the review.
- **Allowed Values:** `approved, rejected, abstained`

## `digest`

- **Type:** `string`
- **Requirement:** Optional
- **Description:** The computed content digest (e.g., sha256:<hex>).
