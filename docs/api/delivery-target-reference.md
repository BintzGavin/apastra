---
title: "Delivery Target Specification"
description: "Schema for delivery target config."
audience: "developers | platform-teams | agents | all"
last_verified: "2026-03-21"
source_files:
  - "promptops/schemas/delivery-target.schema.json"
---

# Delivery Target Specification

Schema for delivery target config.

## Properties

## `type`

- **Type:** `string`
- **Requirement:** Required
- **Description:** Type of delivery target, e.g., 'github_pr', 'oci_registry'

## `repo`

- **Type:** `string`
- **Requirement:** Required
- **Description:** Target repository if type is 'github_pr'
