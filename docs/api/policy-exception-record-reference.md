# policy-exception-record Reference

Schema for policy exception records

## Properties

### `exception_id` (string, Required)
Unique identifier for the exception

### `policy_id` (string, Required)
The policy being bypassed

### `target_digest` (string, Required)
The digest of the package/artifact receiving the exception

### `approver_id` (string, Required)
The person granting the exception

### `reason` (string, Required)
Explanation for the exception

### `timestamp` (string, Required)
Timestamp when the exception was granted

