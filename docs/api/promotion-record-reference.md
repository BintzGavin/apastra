# Promotion Record Specification Reference

Schema for append-only binding records.

## Properties

### `version` (string, Required)
The approved version

### `channel` (string, Required)
The channel to bind to, e.g., 'prod'

### `digest` (string, Required)
The content digest of the version

### `evidence` (object, Optional)
Links to evidence

### `timestamp` (string, Optional)
Timestamp of the promotion

