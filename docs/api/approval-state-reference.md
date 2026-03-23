# approval-state Reference

Schema for an Approval state record indicating human and machine review results.

## Properties

### `revision_ref` (string, Required)
Target digest or ID of the revision or package.

### `checks_passed` (boolean, Required)
Whether the required machine checks have passed.

### `human_review` (object, Required)
Details of the manual human review.

### `decision` (string, Required)
The final decision of the review.
**Enum values:** approved, rejected, abstained

### `digest` (string, Optional)
The computed content digest (e.g., sha256:<hex>).

