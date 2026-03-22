# Deprecation Notices Policy

## 1. Overview
This policy defines the governance procedures for deprecating prompt packages or specific versions within the registry. It enforces an append-only metadata model to ensure consumers receive reliable programmatic signals about sunsetting assets.

## 2. Append-Only Metadata Records
Deprecation of a prompt package or a specific version must be executed by appending an immutable `deprecation-record` to the registry metadata store. In-place modification or deletion of existing packages is strictly prohibited for deprecation purposes.

## 3. Record Requirements
Each `deprecation-record` must conform to the `https://promptops.apastra.com/schemas/deprecation-record.schema.json` schema and include:
-   A unique `deprecation_id`.
-   The exact package name (`reference`) being deprecated.
-   (Optional but recommended) The specific `package_digest` of the version being deprecated.
-   The `timestamp` of the deprecation notice.
-   The `reason` for deprecation.
-   (Optional) A `replacement_ref` pointing to a suggested alternative package.

## 4. Notice Period
A minimum 30-day notice period is required from the timestamp of the deprecation record before any active delivery targets or mirrors cease serving the deprecated artifact. During this period, the artifact remains available but will be flagged as deprecated to consumers.

## 5. Reversal of Deprecation
Reversing a deprecation (un-deprecating) requires appending a new, superseding metadata record that explicitly invalidates the prior `deprecation-record`. Deleting the original deprecation notice is not permitted.
