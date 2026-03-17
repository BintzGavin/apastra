---
title: "Dataset Manifest Reference"
description: "API reference for dataset-manifest schema"
audience: "all"
last_verified: "2026-03-15"
source_files:
  - "promptops/schemas/dataset-manifest.schema.json"
---

# Dataset Manifest Reference

Schema for a dataset manifest, defining identity, version, schema version, digest, and provenance.

## Properties

### `id`
- **Type**: string
- **Presence**: **Required**
- **Description**: Stable identifier for the dataset.

### `version`
- **Type**: string
- **Presence**: **Required**
- **Description**: Semantic version or revision of the dataset.

### `digest`
- **Type**: string
- **Presence**: **Required**
- **Description**: Content digest (e.g., SHA-256) of the associated dataset.jsonl file to ensure reproducibility.

### `schema_version`
- **Type**: string
- **Presence**: **Required**
- **Description**: Version of the dataset case schema used by the JSONL file.

### `provenance`
- **Type**: object
- **Presence**: *Optional*
- **Description**: Information about the origin and creation of the dataset.
