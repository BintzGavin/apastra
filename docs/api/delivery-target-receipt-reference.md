# Delivery Target Receipt Specification Reference

Schema for a delivery target receipt.

## Properties

### `receipt_id` (string, Required)
Unique identifier for the receipt.

### `target_id` (string, Required)
The ID of the delivery target.

### `package_digest` (string, Required)
The SHA-256 digest of the package delivered.

### `timestamp` (string, Required)
The ISO 8601 timestamp of when the delivery was received.

### `status` (string, Required)
The status of the delivery receipt (e.g., success, failed).

### `message` (string, Optional)
Additional information or error message.

### `metadata` (object, Optional)
Key-value pairs of any extra delivery context.
