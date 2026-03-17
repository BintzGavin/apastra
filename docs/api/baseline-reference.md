---
title: "Baseline Reference"
description: "API reference for baseline schema"
audience: "all"
last_verified: "2026-03-15"
source_files:
  - "promptops/schemas/baseline.schema.json"
---

# Baseline Reference

Schema definition for baseline references to unblock Evaluation.

## Properties

### `baseline_id`
- **Type**: string
- **Presence**: **Required**
- **Description**: The baseline ID

### `run_digest`
- **Type**: string
- **Presence**: **Required**
- **Description**: The run digest

### `created_at`
- **Type**: string
- **Presence**: **Required**
- **Description**: The creation time

### `metadata`
- **Type**: object
- **Presence**: *Optional*
- **Description**: The metadata

### `description`
- **Type**: string
- **Presence**: *Optional*
- **Description**: The description
