# Moderation Decision Record Reference

Schema for moderation decision records.

## Properties

### `decision_id` (string, Required)
Unique identifier for the moderation decision.

### `submission_id` (string, Optional)
The ID of the submission this decision applies to.

### `package_digest` (string, Optional)
The SHA-256 digest of the package this decision applies to.

### `decision` (string, Required)
The moderation decision made.
**Enum values:** approved, rejected, flagged

### `moderator_id` (string, Required)
The ID of the moderator who made the decision.

### `timestamp` (string, Required)
The timestamp of the decision.

### `reason` (string, Required)
The reason for the decision.

