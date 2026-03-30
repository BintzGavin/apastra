#### 1. Context & Goal
- **Objective**: Create `community-prompt-pack.schema.json` and its validator to define the schema for curated starter packs.
- **Trigger**: The docs/vision.md expansion 5 specifically requests "Community prompt packs" (curated starter packs like summarization, extraction) to bootstrap the registry.
- **Impact**: Enables the GOVERNANCE and RUNTIME domains to formally package and discover community prompt packs, allowing teams to install pre-built prompts, datasets, and evaluators as git dependencies.

#### 2. File Inventory
- **Create**: `promptops/schemas/community-prompt-pack.schema.json` (JSON Schema for the pack).
- **Create**: `promptops/validators/validate-community-prompt-pack.sh` (Shell script to validate the schema).
- **Modify**: None.
- **Read-Only**: `docs/vision.md` (for community prompt packs definition).

#### 3. Implementation Spec
- **Schema Architecture**: A JSON schema defining a community prompt pack object. Required fields include `id` (stable identifier), `name` (human-readable name), `description` (purpose of the pack), and `custodian` (string, the custodian org managing it). Optional fields could include arrays for `prompts`, `datasets`, `evaluators`, `suites`, and `baselines` containing the references to the files in the pack, as well as `topics` (e.g., summarization, extraction, classification, code review).
- **Validator Logic**: Use `ajv` to validate an input JSON against `community-prompt-pack.schema.json`.
- **Dependencies**: None.

#### 4. Test Plan
- **Verification**: Run `bash promptops/validators/validate-community-prompt-pack.sh test-fixtures/valid-community-prompt-pack.json` where the fixture contains a valid pack configuration.
- **Success Criteria**: The validator exits with status 0, confirming the JSON matches the schema.
- **Edge Cases**: Missing `id`, `name`, `description`, or `custodian` should be rejected. Invalid formats for references should be rejected.
