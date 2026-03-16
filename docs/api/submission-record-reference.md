---
title: "Submission Record Reference"
description: "Schema for an append-only artifact structure for package submissions to a public registry."
audience: "developers | platform-teams | agents | all"
last_verified: "2026-03-11"
source_files:
  - "promptops/schemas/submission-record.schema.json"
---

# Submission Record Reference

Schema for an append-only artifact structure for package submissions to a public registry.

## Properties

## `submission_id`

- **Type:** string
- **Requirement:** Required
- **Description:** Stable identifier for the submission.

## `package_digest`

- **Type:** string
- **Requirement:** Required
- **Description:** Content digest of the submitted package bundle.

## `publisher_id`

- **Type:** string
- **Requirement:** Required
- **Description:** Identifier of the user or system publishing the package.

## `timestamp`

- **Type:** string
- **Requirement:** Required
- **Description:** The time the submission was created.

## `metadata`

- **Type:** object
- **Requirement:** Optional
- **Description:** Arbitrary metadata for the submission.
