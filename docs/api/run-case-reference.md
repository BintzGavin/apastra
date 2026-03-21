---
title: "Run Case Specification"
description: "Schema for a single case in cases.jsonl."
audience: "developers | platform-teams | agents | all"
last_verified: "2026-03-21"
source_files:
  - "promptops/schemas/run-case.schema.json"
---

# Run Case Specification

Schema for a single case in cases.jsonl.

## Properties

## `case_id`

- **Type:** `string`
- **Requirement:** Required
- **Description:** Case ID

## `per_trial_outputs`

- **Type:** `array`
- **Requirement:** Required
- **Description:** Per trial outputs

## `evaluator_outputs`

- **Type:** `array`
- **Requirement:** Required
- **Description:** Evaluator outputs

## `pointers`

- **Type:** `object`
- **Requirement:** Required
- **Description:** Pointers to raw text/traces
