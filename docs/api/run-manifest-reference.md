---
title: "Run Manifest Specification"
description: "Schema for a run manifest."
audience: "developers | platform-teams | agents | all"
last_verified: "2026-03-21"
source_files:
  - "promptops/schemas/run-manifest.schema.json"
---

# Run Manifest Specification

Schema for a run manifest.

## Properties

## `input_refs`

- **Type:** `object`
- **Requirement:** Required
- **Description:** Input references

## `resolved_digests`

- **Type:** `object`
- **Requirement:** Required
- **Description:** Resolved digests

## `timestamps`

- **Type:** `object`
- **Requirement:** Required
- **Description:** Timestamps

## `harness_identifier`

- **Type:** `string`
- **Requirement:** Required
- **Description:** Harness identifier

## `harness_version`

- **Type:** `string`
- **Requirement:** Required
- **Description:** Harness version

## `model_ids`

- **Type:** `array`
- **Requirement:** Required
- **Description:** Model IDs

## `sampling_config`

- **Type:** `object`
- **Requirement:** Required
- **Description:** Sampling configuration

## `environment`

- **Type:** `object`
- **Requirement:** Required
- **Description:** Environment metadata

## `status`

- **Type:** `string`
- **Requirement:** Required
- **Description:** Run status

## `provenance`

- **Type:** `object`
- **Requirement:** Optional
- **Description:** SLSA-style provenance metadata representing the invocation of the evaluation run.
