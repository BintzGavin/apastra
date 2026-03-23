# Deprecation Record Reference

Schema for deprecation records.

## Properties

### `deprecation_id` (string, Required)
Unique identifier for the deprecation record.

### `package_digest` (string, Optional)
The SHA-256 digest of the deprecated package.

### `reference` (string, Optional)
The reference of the deprecated package.

### `timestamp` (string, Required)
The timestamp of the deprecation.

### `reason` (string, Required)
The reason for the deprecation.

### `replacement_ref` (string, Optional)
The reference to the suggested replacement.

