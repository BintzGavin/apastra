---
title: "Emergency Takedown Decision"
description: "Schema for an emergency takedown decision."
audience: "developers | platform-teams | agents | all"
last_verified: "2026-03-22"
source_files:
  - "promptops/schemas/emergency-takedown-decision.schema.json"
---

# Emergency Takedown Decision

Schema for an emergency takedown decision.

## Properties

### `decision_id`

- **Type:** `string`
- **Requirement:** Required
- **Description:** Unique identifier for the takedown decision.

### `authorizer_id`

- **Type:** `string`
- **Requirement:** Required
- **Description:** Identifier of the individual who authorized the takedown.

### `timestamp`

- **Type:** `string`
- **Requirement:** Required
- **Description:** The timestamp of the decision.

### `justification`

- **Type:** `string`
- **Requirement:** Required
- **Description:** The justification for the emergency takedown.

### `action_taken`

- **Type:** `string`
- **Requirement:** Required
- **Description:** The specific action taken, e.g., 'immediate_removal'.

### `package_digest`

- **Type:** `string`
- **Requirement:** Optional
- **Description:** The SHA-256 digest of the affected package.

### `target_reference`

- **Type:** `string`
- **Requirement:** Optional
- **Description:** A reference to the target if a package digest is not applicable.
