---
title: "Ownership Dispute Record Reference"
description: "Schema for an ownership dispute record in the governance system."
audience: "developers | platform-teams | agents | all"
last_verified: "2026-03-21"
source_files:
  - "promptops/schemas/ownership-dispute-record.schema.json"
---

# Ownership Dispute Record Reference

Schema for an ownership dispute record in the governance system.

## Properties

## `dispute_id`

- **Type:** `string`
- **Requirement:** Required
- **Description:** Unique identifier for the dispute.

## `package_name`

- **Type:** `string`
- **Requirement:** Required
- **Description:** The canonical name of the package in dispute.

## `complainant_id`

- **Type:** `string`
- **Requirement:** Required
- **Description:** Identifier of the party filing the dispute.

## `timestamp`

- **Type:** `string`
- **Requirement:** Required
- **Description:** Timestamp when the dispute was created.

## `claim_reason`

- **Type:** `string`
- **Requirement:** Required
- **Description:** The detailed reason for the ownership claim.

## `status`

- **Type:** `string`
- **Requirement:** Required
- **Description:** Current status of the dispute.
- **Allowed Values:** `open, under_review, resolved`

## `evidence_links`

- **Type:** `array`
- **Requirement:** Optional
- **Description:** Optional list of URLs containing evidence supporting the claim.

## `resolution_notes`

- **Type:** `string`
- **Requirement:** Optional
- **Description:** Notes added upon resolution of the dispute.
