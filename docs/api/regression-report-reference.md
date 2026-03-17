---
title: "Regression Report Reference"
description: "API reference for regression-report schema"
audience: "all"
last_verified: "2026-03-15"
source_files:
  - "promptops/schemas/regression-report.schema.json"
---

# Regression Report Reference

Schema for a regression report output.

## Properties

### `status`
- **Type**: string
- **Presence**: **Required**
- **Description**: Pass, fail, warning status

### `baseline_ref`
- **Type**: string
- **Presence**: **Required**
- **Description**: The reference digest or ID

### `candidate_ref`
- **Type**: string
- **Presence**: **Required**
- **Description**: The digest or ID being tested

### `evidence`
- **Type**: array of object
- **Presence**: **Required**
- **Description**: A list of metric deltas and comparisons
