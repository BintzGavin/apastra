---
title: "Regression Policy Specification"
description: "Schema for regression policy definition."
audience: "developers | platform-teams | agents | all"
last_verified: "2026-03-21"
source_files:
  - "promptops/schemas/regression-policy.schema.json"
---

# Regression Policy Specification

Schema for regression policy definition.

## Properties

## `baseline`

- **Type:** `string`
- **Requirement:** Required
- **Description:** Baseline reference rules, e.g., 'prod current'

## `rules`

- **Type:** `array`
- **Requirement:** Required
- **Description:** List of per-metric rules
