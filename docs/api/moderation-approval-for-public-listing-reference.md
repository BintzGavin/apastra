# Moderation Approval for Public Listing Reference

Schema for moderation approval for public listing records.

## Properties

### `approval_id` (string, Required)
Unique identifier for the moderation approval.

### `package_digest` (string, Required)
The SHA-256 digest of the package being approved.

### `approver_id` (string, Required)
The ID of the moderator who approved the listing.

### `timestamp` (string, Required)
The timestamp of the approval.

### `listing_tier` (string, Required)
The tier of the public listing.

