---
title: "Release Descriptor Reference"
description: "Schema for a release descriptor, posted to an internal API as part of abstract delivery targets."
audience: "developers | platform-teams | agents"
last_verified: "2024-05-24"
source_files:
  - "promptops/schemas/release-descriptor.schema.json"
---

# Release Descriptor Reference

Schema for a release descriptor, posted to an internal API as part of abstract delivery targets.

## Schema Details

### `descriptor_id`

- **Type**: string
- **Required**: Yes
- **Description**: Unique identifier for this release descriptor

### `timestamp`

- **Type**: string
- **Required**: Yes
- **Description**: ISO-8601 timestamp of when the descriptor was created

### `prompt_digest`

- **Type**: string
- **Required**: Yes
- **Description**: The canonical digest of the prompt package being released

### `prompt_version`

- **Type**: string
- **Required**: No
- **Description**: Semantic version of the prompt package being released, if applicable

### `environment`

- **Type**: string
- **Required**: Yes
- **Description**: The environment this release is targeting (e.g., prod, staging)

### `signatures`

- **Type**: array of object
- **Required**: Yes
- **Description**: Digital signatures ensuring the authenticity of the release

### `metadata`

- **Type**: object
- **Required**: No
- **Description**: Additional metadata related to the release descriptor
