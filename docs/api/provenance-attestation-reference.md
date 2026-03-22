---
title: "Provenance Attestation"
description: "Schema for supply-chain provenance attestations (SLSA-style)."
audience: "developers | platform-teams | agents | all"
last_verified: "2026-03-22"
source_files:
  - "promptops/schemas/provenance-attestation.schema.json"
---

# Provenance Attestation

Schema for supply-chain provenance attestations (SLSA-style).

## Properties

### `attestation_id`

- **Type:** `string`
- **Requirement:** Required
- **Description:** Unique identifier for the attestation.

### `subject`

- **Type:** `array`
- **Requirement:** Required
- **Description:** The artifacts that are the subject of the attestation.
- **Items Type:** `object`

### `predicateType`

- **Type:** `string`
- **Requirement:** Required
- **Description:** URI indicating the format of the predicate (e.g., SLSA Provenance).

### `predicate`

- **Type:** `object`
- **Requirement:** Required
- **Description:** The detailed attestation predicate containing builder, invocation, and materials.
