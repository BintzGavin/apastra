# Takedown Appeal Record Reference

A record used to formally process and track appeals to moderation takedowns.

## Properties

### `appeal_id` (string, Required)
Unique identifier for this takedown appeal.

### `takedown_record_id` (string, Required)
Reference to the original takedown record being appealed.

### `appellant_id` (string, Required)
Identifier of the user or entity filing the appeal.

### `reasoning` (string, Required)
Text reasoning explaining why the takedown should be overturned.

### `status` (string, Required)
Current status of the appeal.
**Enum values:** pending, approved, rejected

### `evidence_links` (array[string], Optional)
Optional array of links providing evidence to support the appeal.

