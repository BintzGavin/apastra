---
title: "Regression Report Specification Reference"
description: "Schema for a regression report output."
audience: "developers | platform-teams | agents | all"
last_verified: "2026-03-20"
source_files:
  - "promptops/schemas/regression-report.schema.json"
---

# Regression Report Specification Reference

Schema for a regression report output.

## Properties

## `status`

- **Type:** string
- **Requirement:** Required
- **Description:** Pass, fail, warning status

## `baseline_ref`

- **Type:** string
- **Requirement:** Required
- **Description:** The reference digest or ID

## `candidate_ref`

- **Type:** string
- **Requirement:** Required
- **Description:** The digest or ID being tested

## `evidence`

- **Type:** array of object
- **Requirement:** Required
- **Description:** A list of metric deltas and comparisons

