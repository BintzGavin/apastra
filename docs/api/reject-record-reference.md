---
title: "Reject Record"
description: "A record used to formally track rejected prompt package submissions."
audience: "all"
last_verified: "2026-04-05"
source_files:
  - "promptops/schemas/reject-record.schema.json"
---

# Reject Record

A record used to formally track rejected prompt package submissions.

## Properties

### `record_id` (Required)

**Type:** `string`

Unique identifier for this reject record.

### `submission_id` (Required)

**Type:** `string`

Reference to the original submission being rejected.

### `package_digest` (Required)

**Type:** `string`

The SHA-256 digest of the rejected package.

### `reasons` (Required)

**Type:** `array`

An array of text reasons explaining why the submission was rejected.

### `moderator_id` (Required)

**Type:** `string`

Identifier of the moderator rejecting the submission.

### `timestamp` (Required)

**Type:** `string`

Timestamp indicating when the rejection occurred.
