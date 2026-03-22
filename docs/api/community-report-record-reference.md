---
title: "Community Report Record"
description: "Schema for a community report record in the governance system."
audience: "developers | platform-teams | agents | all"
last_verified: "2026-03-22"
source_files:
  - "promptops/schemas/community-report-record.schema.json"
---

# Community Report Record

Schema for a community report record in the governance system.

## Properties

### `report_id`

- **Type:** `string`
- **Requirement:** Required
- **Description:** Unique identifier for the report.

### `target_package_name`

- **Type:** `string`
- **Requirement:** Required
- **Description:** The canonical name of the package or model being reported.

### `reporter_id`

- **Type:** `string`
- **Requirement:** Required
- **Description:** Identifier of the party filing the report.

### `timestamp`

- **Type:** `string`
- **Requirement:** Required
- **Description:** Timestamp when the report was created.

### `reason_category`

- **Type:** `string`
- **Requirement:** Required
- **Description:** The categorization of the issue being reported.
- **Allowed Values:** `malware`, `hate_speech`, `pii_leak`, `spam`, `other`

### `status`

- **Type:** `string`
- **Requirement:** Required
- **Description:** Current status of the report.
- **Allowed Values:** `open`, `under_review`, `resolved`

### `evidence_links`

- **Type:** `array`
- **Requirement:** Optional
- **Description:** Optional list of URLs containing evidence supporting the report.
- **Items Type:** `string`

### `detailed_description`

- **Type:** `string`
- **Requirement:** Optional
- **Description:** Optional detailed narrative explaining the report.
