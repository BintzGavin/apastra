---
title: "Namespace Claim Record"
description: "Schema for a namespace claim record, used to track canonical name registrations, ownership disputes, and deprecations."
audience: "developers | platform-teams | agents | all"
last_verified: "2026-03-22"
source_files:
  - "promptops/schemas/namespace-claim-record.schema.json"
---

# Namespace Claim Record

Schema for a namespace claim record, used to track canonical name registrations, ownership disputes, and deprecations.

## Properties

### `claim_id`

- **Type:** `string`
- **Requirement:** Required
- **Description:** A unique identifier for the namespace claim request.

### `namespace`

- **Type:** `string`
- **Requirement:** Required
- **Description:** The requested canonical namespace. Must contain only lowercase letters, numbers, and hyphens.

### `requester_id`

- **Type:** `string`
- **Requirement:** Required
- **Description:** The identifier of the user or organization requesting the namespace claim.

### `timestamp`

- **Type:** `string`
- **Requirement:** Required
- **Description:** The ISO-8601 formatted timestamp of when the claim was made.

### `status`

- **Type:** `string`
- **Requirement:** Required
- **Description:** The current status of the namespace claim request.
- **Allowed Values:** `pending`, `approved`, `rejected`, `disputed`

### `evidence_uri`

- **Type:** `string`
- **Requirement:** Optional
- **Description:** An optional URI providing proof of trademark or ownership for the requested namespace.
