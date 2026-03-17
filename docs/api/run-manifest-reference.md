---
title: "Run Manifest Reference"
description: "API reference for run-manifest schema"
audience: "all"
last_verified: "2026-03-15"
source_files:
  - "promptops/schemas/run-manifest.schema.json"
---

# Run Manifest Reference

Schema for a run manifest.

## Properties

### `input_refs`
- **Type**: object
- **Presence**: **Required**
- **Description**: Input references

### `resolved_digests`
- **Type**: object
- **Presence**: **Required**
- **Description**: Resolved digests

### `timestamps`
- **Type**: object
- **Presence**: **Required**
- **Description**: Timestamps

### `harness_identifier`
- **Type**: string
- **Presence**: **Required**
- **Description**: Harness identifier

### `harness_version`
- **Type**: string
- **Presence**: **Required**
- **Description**: Harness version

### `model_ids`
- **Type**: array of string
- **Presence**: **Required**
- **Description**: Model IDs

### `sampling_config`
- **Type**: object
- **Presence**: **Required**
- **Description**: Sampling configuration

### `environment`
- **Type**: object
- **Presence**: **Required**
- **Description**: Environment metadata

### `status`
- **Type**: string
- **Presence**: **Required**
- **Description**: Run status

### `provenance`
- **Type**: object
- **Presence**: *Optional*
- **Description**: SLSA-style provenance metadata representing the invocation of the evaluation run.

### `provenance.builder`
- **Type**: object
- **Presence**: *Optional*
- **Description**: Identifies the builder.

### `provenance.builder.id`
- **Type**: string
- **Presence**: *Optional*
- **Description**: String URI identifying the builder.

### `provenance.buildType`
- **Type**: string
- **Presence**: *Optional*
- **Description**: String defining the build model.

### `provenance.invocation`
- **Type**: object
- **Presence**: *Optional*
- **Description**: Invocation configuration.

### `provenance.invocation.configSource`
- **Type**: object
- **Presence**: *Optional*
- **Description**: Source of the configuration.

### `provenance.invocation.environment`
- **Type**: object
- **Presence**: *Optional*
- **Description**: Invocation environment.

### `provenance.metadata`
- **Type**: object
- **Presence**: *Optional*
- **Description**: Timestamps and build metadata.
