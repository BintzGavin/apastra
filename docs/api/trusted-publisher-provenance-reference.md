---
title: "Trusted Publisher Provenance"
description: "Provenance record to verify and grant trusted publisher badges for packages and providers."
audience: "developers | platform-teams | agents | all"
last_verified: "2026-03-22"
source_files:
  - "promptops/schemas/trusted-publisher-provenance.schema.json"
---

# Trusted Publisher Provenance

Provenance record to verify and grant trusted publisher badges for packages and providers.

## Properties

### `publisher_id`

- **Type:** `string`
- **Requirement:** Required
- **Description:** Unique identifier of the trusted publisher.

### `package_name`

- **Type:** `string`
- **Requirement:** Required
- **Description:** Name or canonical digest of the package being published.

### `timestamp`

- **Type:** `string`
- **Requirement:** Required
- **Description:** Time the provenance record was generated.

### `claims`

- **Type:** `object`
- **Requirement:** Required
- **Description:** Verifications performed for trusted publisher badging.
