# Mirror Sync Receipt Reference

Schema for mirror sync receipts.

## Properties

### `receipt_id` (string, Required)
Unique identifier for the sync receipt.

### `mirror_id` (string, Required)
The ID of the mirror.

### `synced_digests` (array[string], Required)
Array of SHA-256 digests that were synced.

### `timestamp` (string, Required)
The timestamp of the sync.

### `status` (string, Required)
The status of the sync operation.

