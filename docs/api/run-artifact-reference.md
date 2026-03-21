---
title: "Run Artifact Specification"
description: "Schema for a minimal BYO harness run artifact output."
audience: "developers | platform-teams | agents | all"
last_verified: "2026-03-21"
source_files:
  - "promptops/schemas/run-artifact.schema.json"
---

# Run Artifact Specification

Schema for a minimal BYO harness run artifact output.

## Properties

## `manifest`

- **Type:** `object`
- **Requirement:** Required
- **Description:** Run manifest

## `scorecard`

- **Type:** `object`
- **Requirement:** Required
- **Description:** Run scorecard

## `cases`

- **Type:** `array`
- **Requirement:** Required
- **Description:** Run cases

## `failures`

- **Type:** `array`
- **Requirement:** Required
- **Description:** Run failures
