# Namespace Claim Record Reference

Schema for a namespace claim record, used to track canonical name registrations, ownership disputes, and deprecations.

## Properties

### `claim_id` (string, Required)
A unique identifier for the namespace claim request.

### `namespace` (string, Required)
The requested canonical namespace. Must contain only lowercase letters, numbers, and hyphens.

### `requester_id` (string, Required)
The identifier of the user or organization requesting the namespace claim.

### `timestamp` (string, Required)
The ISO-8601 formatted timestamp of when the claim was made.

### `status` (string, Required)
The current status of the namespace claim request.
**Enum values:** pending, approved, rejected, disputed

### `evidence_uri` (string, Optional)
An optional URI providing proof of trademark or ownership for the requested namespace.

