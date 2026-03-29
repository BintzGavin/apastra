---
title: "Drift Report Specification Reference"
description: "Schema for a drift report comparing current results vs a baseline to identify output drift."
audience: "developers | platform-teams | agents"
last_verified: "2024-05-24"
source_files:
  - "promptops/schemas/drift-report.schema.json"
---

# Drift Report Specification Reference

Schema for a drift report comparing current results vs a baseline to identify output drift.

## Schema Details

### `baseline_ref`

- **Type**: string
- **Required**: Yes
- **Description**: The reference digest or ID for the baseline.

### `current_ref`

- **Type**: string
- **Required**: Yes
- **Description**: The current digest or ID being tested for drift.

### `drift_detected`

- **Type**: boolean
- **Required**: Yes
- **Description**: Boolean indicating if drift was detected beyond acceptable thresholds.

### `evidence`

- **Type**: array of object
- **Required**: Yes
- **Description**: A list of metric comparisons and delta details for detected drift.
