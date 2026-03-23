# Emergency Takedown Decision Reference

Schema for an emergency takedown decision.

## Properties

### `decision_id` (string, Required)
Unique identifier for the takedown decision.

### `authorizer_id` (string, Required)
Identifier of the individual who authorized the takedown.

### `timestamp` (string, Required)
The timestamp of the decision.

### `justification` (string, Required)
The justification for the emergency takedown.

### `action_taken` (string, Required)
The specific action taken, e.g., 'immediate_removal'.

### `package_digest` (string, Optional)
The SHA-256 digest of the affected package.

### `target_reference` (string, Optional)
A reference to the target if a package digest is not applicable.

