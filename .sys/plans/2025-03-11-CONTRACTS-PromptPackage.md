#### 1. Context & Goal
- **Objective**: Create JSON schema for Prompt Package manifest and validation script.
- **Trigger**: `README.md` defines Prompt Package as an immutable bundle of prompt specs with a manifest and content digest, but `promptops/schemas/` currently lacks `prompt-package.schema.json`.
- **Impact**: Unlocks governed release packaging options (OCI, npm, PyPI) and allows the RUNTIME domain's Git-first resolver to resolve packaged artifacts.

#### 2. File Inventory
- **Create**: `promptops/schemas/prompt-package.schema.json` (JSON Schema for the manifest), `promptops/validators/validate-prompt-package.sh` (Shell script to validate manifest against schema)
- **Modify**: `docs/status/CONTRACTS.md` (Update version and log completion)
- **Read-Only**: `README.md`, `promptops/schemas/digest-convention.md`

#### 3. Implementation Spec
- **Schema Architecture**: JSON Schema defining the manifest. Must include `id` (stable package ID), `digest` (content digest of the package), `specs` (array of included prompt spec IDs/digests), and optionally `version` (semver) and `metadata` (provenance, etc.).
- **Content Digest Convention**: As defined in `digest-convention.md`, computed using SHA-256 over canonicalized JSON. Stored in the `digest` field.
- **Pseudo-Code**: Validation flow reads `prompt-package.schema.json` and uses `ajv-cli` to validate a given `manifest.json`.
- **Public Contract Changes**: Exports `apastra-prompt-package-v1` schema ID.
- **Dependencies**: Depends on the existing prompt-spec schema. No cross-domain blockers.

#### 4. Test Plan
- **Verification**: `mkdir -p test-fixtures && echo '{"id":"pkg1", "digest":"sha256:abcd", "specs":[]}' > test-fixtures/valid-prompt-package.json && npx ajv-cli validate -s promptops/schemas/prompt-package.schema.json -d test-fixtures/valid-prompt-package.json --spec=draft2020 --strict=false`
- **Success Criteria**: `[ $? -eq 0 ]`
- **Edge Cases**: `echo '{"id":"pkg1"}' > test-fixtures/invalid-prompt-package.json && npx ajv-cli validate -s promptops/schemas/prompt-package.schema.json -d test-fixtures/invalid-prompt-package.json --spec=draft2020 --strict=false; [ $? -ne 0 ]`