---
title: "Delivery Target Reference"
description: "API reference for delivery-target schema"
audience: "all"
last_verified: "2026-03-15"
source_files:
  - "promptops/schemas/delivery-target.schema.json"
---

# Delivery Target Reference

Schema for delivery target config.

## Properties

### `type`
- **Type**: string
- **Presence**: **Required**
- **Description**: Type of delivery target, e.g., 'github_pr', 'oci_registry'

### `repo`
- **Type**: string
- **Presence**: **Required**
- **Description**: Target repository if type is 'github_pr'
