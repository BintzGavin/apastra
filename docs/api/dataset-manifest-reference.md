---
title: "Dataset Manifest Reference"
description: "Schema for a dataset manifest, defining identity, version, schema version, digest, and provenance."
audience: "developers | platform-teams | agents | all"
last_verified: "2026-03-11"
source_files:
  - "promptops/schemas/dataset-manifest.schema.json"
---

# Dataset Manifest Reference

Schema for a dataset manifest, defining identity, version, schema version, digest, and provenance.

## Properties

## `id`

- **Type:** string
- **Requirement:** Required
- **Description:** Stable identifier for the dataset.

## `version`

- **Type:** string
- **Requirement:** Required
- **Description:** Semantic version or revision of the dataset.

## `digest`

- **Type:** string
- **Requirement:** Required
- **Description:** Content digest (e.g., SHA-256) of the associated dataset.jsonl file to ensure reproducibility.

## `schema_version`

- **Type:** string
- **Requirement:** Required
- **Description:** Version of the dataset case schema used by the JSONL file.
