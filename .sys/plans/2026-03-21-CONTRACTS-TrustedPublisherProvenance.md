#### 1. Context & Goal
- **Objective**: Create a JSON Schema and validation script for trusted publisher provenance records.
- **Trigger**: `docs/vision.md` explicitly calls for "provenance requirements for 'trusted publisher' badges" in Phase 4 (Moderation and governance hardening), but no corresponding schema exists in `promptops/schemas/`.
- **Impact**: Enables the GOVERNANCE and RUNTIME domains to formally generate, validate, and track provenance claims required to grant or verify trusted publisher badges for packages and providers.

#### 2. File Inventory
- **Create**:
  - `promptops/schemas/trusted-publisher-provenance.schema.json`: JSON schema defining the structure for a trusted publisher provenance record.
  - `promptops/validators/validate-trusted-publisher-provenance.sh`: Bash script to validate a provenance JSON instance against the schema.
- **Modify**: None
- **Read-Only**: None

#### 3. Implementation Spec
- **Schema Architecture**: Define a JSON Schema structure representing provenance. Required fields should include `publisher_id`, `package_name` (or `package_digest`), `timestamp`, and a `claims` object. The `claims` object should specify the verifications performed (e.g., `identity_verified`, `source_repo_linked`, `build_environment_attested`), each containing a boolean status and optional `evidence_url` or `signature` fields.
- **Content Digest Convention**: The schema definition file itself will not dictate how digests are computed for the instances, but instances adhering to this schema could be hashed using the canonical JSON SHA-256 convention if signed.
- **Pseudo-Code**:
  1. Define the complete JSON Schema representing the structured provenance record.
  2. Write a shell script using `ajv` to validate an input JSON payload against the `trusted-publisher-provenance.schema.json` file.
- **Public Contract Changes**: Exports the `trusted-publisher-provenance.schema.json` to define the formal contract for trusted publisher provenance metadata.
- **Dependencies**: None.
