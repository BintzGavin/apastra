# Takedown Policy

This policy defines the process for handling takedown requests for prompts in the public registry. Takedowns may be initiated for copyright violations, moderation violations, or other valid legal or community concerns. Takedown requests must provide specific evidence.

## Append-Only Record Requirement

All takedowns must generate an append-only JSON record conforming to the takedown-record.schema.json. Modifying existing records is prohibited. The record serves as the auditable source of truth for the takedown action and must be stored in the registry metadata store.

### Required Schema Fields

The JSON document must strictly adhere to promptops/schemas/takedown-record.schema.json and include the following:
- takedown_id: Unique identifier for the takedown record.
- package_digest: The SHA-256 digest of the taken down package.
- timestamp: The timestamp of the takedown.
- reason: The reason for the takedown.
- policy_violation_type: The type of policy violation.
