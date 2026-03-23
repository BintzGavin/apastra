# Moderation Escalation Record Reference

Schema for a moderation escalation record.

## Properties

### `escalation_id` (string, Required)
Unique identifier for the escalation.

### `submission_id` (string, Required)
Unique identifier for the submission.

### `escalated_by` (string, Required)
User who escalated the content.

### `reason` (string, Required)
Reason for the escalation.

### `timestamp` (string, Required)
Timestamp of the escalation.

### `status` (string, Required)
Status of the escalation.
**Enum values:** pending, reviewed, dismissed

### `reviewer_id` (string, Optional)
User who reviewed the escalation.

### `notes` (string, Optional)
Additional notes.

