---
title: "Submission Record Reference"
description: "API reference for submission-record schema"
audience: "all"
last_verified: "2026-03-15"
source_files:
  - "promptops/schemas/submission-record.schema.json"
---

# Submission Record Reference

Schema for an append-only artifact structure for package submissions to a public registry.

## Properties

### `submission_id`
- **Type**: string
- **Presence**: **Required**
- **Description**: Stable identifier for the submission.

### `package_digest`
- **Type**: string
- **Presence**: **Required**
- **Description**: Content digest of the submitted package bundle.

### `publisher_id`
- **Type**: string
- **Presence**: **Required**
- **Description**: Identifier of the user or system publishing the package.

### `timestamp`
- **Type**: string
- **Presence**: **Required**
- **Description**: The time the submission was created.

### `metadata`
- **Type**: object
- **Presence**: *Optional*
- **Description**: Arbitrary metadata for the submission.
