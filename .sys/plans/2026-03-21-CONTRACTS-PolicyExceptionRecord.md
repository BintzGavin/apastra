#### 1. Context & Goal
- **Objective**: Create a JSON Schema and bash validator for policy exception records.
- **Trigger**: `docs/vision.md` explicitly lists "Policy exceptions" as a component of human checkpoints in the single-custodian registry model, which requires an append-only metadata record schema.
- **Impact**: Unlocks the ability for the GOVERNANCE and RUNTIME domains to issue, track, and verify human-approved exceptions to automated policies programmatically without state hallucination.

#### 2. File Inventory
- **Create**:
  - `promptops/schemas/policy-exception-record.schema.json`
  - `promptops/validators/validate-policy-exception-record.sh`
- **Modify**: None
- **Read-Only**:
  - `docs/vision.md`

#### 3. Implementation Spec
- **Schema Architecture**: JSON Schema defining `exception_id` (unique string), `policy_id` (the policy being bypassed), `target_digest` (the digest of the package/artifact receiving the exception), `approver_id` (the person granting the exception), `reason` (string explanation), and `timestamp` (date-time format). Ensure strict validation of all fields.
- **Content Digest Convention**: The exception record itself is append-only, wrapping a specific `target_digest`.
- **Pseudo-Code**: Validate the JSON input against `policy-exception-record.schema.json` using `ajv`. If valid, exit 0; else, exit 1.
- **Public Contract Changes**: Exports `https://promptops.apastra.com/schemas/policy-exception-record.schema.json`.
- **Dependencies**: None.
