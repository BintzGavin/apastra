---
title: "Run Manifest Specification Reference"
description: "Schema for a run manifest."
audience: "developers | platform-teams | agents | all"
last_verified: "2026-03-11"
source_files:
  - "promptops/schemas/run-manifest.schema.json"
---

# Run Manifest Specification Reference

Schema for a run manifest.

## Properties

## `input_refs`

- **Type:** object
- **Requirement:** Required
- **Description:** Input references

## `resolved_digests`

- **Type:** object
- **Requirement:** Required
- **Description:** Resolved digests

## `timestamps`

- **Type:** object
- **Requirement:** Required
- **Description:** Timestamps

## `harness_version`

- **Type:** string
- **Requirement:** Required
- **Description:** Harness version

## `model_ids`

- **Type:** array of string
- **Requirement:** Required
- **Description:** Model IDs

## `environment`

- **Type:** object
- **Requirement:** Required
- **Description:** Environment metadata

## `status`

- **Type:** string
- **Requirement:** Required
- **Description:** Run status
