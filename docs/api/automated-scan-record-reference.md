---
title: "Automated Scan Record"
description: "A record of an automated scan performed on a prompt package."
audience: "developers | platform-teams | agents | all"
last_verified: "2026-03-22"
source_files:
  - "promptops/schemas/automated-scan-record.schema.json"
---

# Automated Scan Record

A record of an automated scan performed on a prompt package.

## Properties

### `scan_id`

- **Type:** `string`
- **Requirement:** Required
- **Description:** Unique identifier for this scan record.

### `package_digest`

- **Type:** `string`
- **Requirement:** Required
- **Description:** The digest of the package that was scanned.

### `timestamp`

- **Type:** `string`
- **Requirement:** Required
- **Description:** When the scan was performed.

### `scanner_id`

- **Type:** `string`
- **Requirement:** Required
- **Description:** The tool or service performing the scan.

### `scan_type`

- **Type:** `string`
- **Requirement:** Required
- **Description:** The type of scan performed.
- **Allowed Values:** `malware`, `secrets`, `schema`, `policy`

### `result`

- **Type:** `string`
- **Requirement:** Required
- **Description:** The outcome of the scan.
- **Allowed Values:** `pass`, `fail`, `warn`

### `evidence_links`

- **Type:** `array`
- **Requirement:** Optional
- **Description:** Optional links to detailed scan logs or evidence.
- **Items Type:** `string`

### `detailed_report`

- **Type:** `string`
- **Requirement:** Optional
- **Description:** Optional detailed text report from the scanner.
