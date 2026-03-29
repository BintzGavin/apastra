#### 1. Context & Goal
- **Objective**: Create a JSON schema for a release descriptor.
- **Trigger**: The docs/vision.md requires a "release descriptor" to be posted to an internal API as part of abstract delivery targets.
- **Impact**: Enables the GOVERNANCE domain to correctly post signed release descriptors.

#### 2. File Inventory
- **Create**: `promptops/schemas/release-descriptor.schema.json`, `promptops/validators/validate-release-descriptor.sh`
- **Modify**: None
- **Read-Only**: `docs/vision.md`

#### 3. Implementation Spec
- **Schema Architecture**: The schema should include standard metadata (ID, timestamp), references to the exact prompt versions (digest, semantic version), details on the environment for which this is released, and the digital signatures to ensure authenticity.
- **Content Digest Convention**: Standard JSON digest convention.
- **Pseudo-Code**: A shell script `validate-release-descriptor.sh` which uses `ajv` to validate incoming `.json` files against the newly created schema.
- **Public Contract Changes**: New schema `apastra-release-descriptor-v1` exported.
- **Dependencies**: Depends on the GOVERNANCE and RUNTIME components properly utilizing this format.

#### 4. Test Plan
- **Verification**: `ajv validate -s promptops/schemas/release-descriptor.schema.json -d <test-fixture>`
- **Success Criteria**: AJV successfully returns true for a valid test fixture.
- **Edge Cases**: Fails gracefully with invalid objects, missing digest, or missing signature arrays.
