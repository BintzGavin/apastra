# ownership-dispute-record Reference

Schema for an ownership dispute record in the governance system.

## Properties

### `dispute_id` (string, Required)
Unique identifier for the dispute.

### `package_name` (string, Required)
The canonical name of the package in dispute.

### `complainant_id` (string, Required)
Identifier of the party filing the dispute.

### `timestamp` (string, Required)
Timestamp when the dispute was created.

### `claim_reason` (string, Required)
The detailed reason for the ownership claim.

### `status` (string, Required)
Current status of the dispute.
**Enum values:** open, under_review, resolved

### `evidence_links` (array[string], Optional)
Optional list of URLs containing evidence supporting the claim.

### `resolution_notes` (string, Optional)
Notes added upon resolution of the dispute.

