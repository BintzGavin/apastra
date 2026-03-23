# Submission Record Reference

Schema for an append-only artifact structure for package submissions to a public registry.

## Properties

### `submission_id` (string, Required)
Stable identifier for the submission.

### `package_digest` (string, Required)
Content digest of the submitted package bundle.

### `publisher_id` (string, Required)
Identifier of the user or system publishing the package.

### `timestamp` (string, Required)
The time the submission was created.

### `metadata` (object, Optional)
Arbitrary metadata for the submission.

