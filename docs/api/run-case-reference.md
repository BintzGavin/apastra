---
title: "Run Case Reference"
description: "API reference for run-case schema"
audience: "all"
last_verified: "2026-03-15"
source_files:
  - "promptops/schemas/run-case.schema.json"
---

# Run Case Reference

Schema for a single case in cases.jsonl.

## Properties

### `case_id`
- **Type**: string
- **Presence**: **Required**
- **Description**: Case ID

### `per_trial_outputs`
- **Type**: array
- **Presence**: **Required**
- **Description**: Per trial outputs

### `evaluator_outputs`
- **Type**: array
- **Presence**: **Required**
- **Description**: Evaluator outputs

### `pointers`
- **Type**: object
- **Presence**: **Required**
- **Description**: Pointers to raw text/traces
