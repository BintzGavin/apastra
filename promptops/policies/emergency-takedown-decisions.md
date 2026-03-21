# Emergency Takedown Decisions Policy

## 1. Objective
This policy defines the criteria and procedure for executing an emergency takedown of a prompt package from the single-custodian registry.

## 2. Emergency Criteria
An emergency takedown bypasses standard review timelines (e.g., the 48-hour notice period) when a prompt package poses a severe and immediate risk to the ecosystem. Examples include:
- Explicit CSAM
- Active malware propagation
- Immediate legal injunction

## 3. Execution Procedure
If a package meets the emergency criteria:
1. **Out-of-Band Alert**: Emergency takedown reports require an immediate out-of-band alert to governance administrators.
2. **Authorization**: The takedown must be immediately authorized and executed by a senior governance maintainer.
3. **Bypass**: The standard review and appeal waiting period is suspended.
4. **Record Creation**: Upon validation, the admin directly commits a `takedown-record.schema.json` document to the registry metadata store detailing the action.

## 4. Required Records
Every emergency takedown must generate a formal `takedown-record.schema.json` containing:
- A unique `takedown_id`
- The `package_digest` of the affected asset
- A `timestamp` of the action
- The specific `reason` justifying the emergency bypass
- The `policy_violation_type`

## 5. Review Boundaries
Updates to this policy are governed by the `promptops/policies/ @apastra/governance-admins` CODEOWNERS boundary.

## 6. Edge Cases
Instances where the emergency criteria are not met must gracefully fall back to the standard `takedown.md` process.
