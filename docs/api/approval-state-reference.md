---
title: "Approval State Reference"
description: "API reference for approval-state schema"
audience: "all"
last_verified: "2026-03-15"
source_files:
  - "promptops/schemas/approval-state.schema.json"
---

# Approval State Reference

Schema for an Approval state record indicating human and machine review results.

## Properties

### `revision_ref`
- **Type**: string
- **Presence**: **Required**
- **Description**: Target digest or ID of the revision or package.

### `checks_passed`
- **Type**: boolean
- **Presence**: **Required**
- **Description**: Whether the required machine checks have passed.

### `human_review`
- **Type**: object
- **Presence**: **Required**
- **Description**: Details of the manual human review.

### `human_review.reviewer`
- **Type**: string
- **Presence**: **Required**
- **Description**: The identity of the reviewer.

### `human_review.timestamp`
- **Type**: string
- **Presence**: **Required**
- **Description**: The time when the review occurred.

### `decision`
- **Type**: enum (`approved`, `rejected`, `abstained`)
- **Presence**: **Required**
- **Description**: The final decision of the review.

### `digest`
- **Type**: string
- **Presence**: *Optional*
- **Description**: The computed content digest (e.g., sha256:<hex>).
