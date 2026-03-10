#### 1. Context & Goal
- **Objective**: Create the JSON schema for the consumption manifest (`consumption.yaml`).
- **Trigger**: Appendix D in `README.md` requires a `consumption.yaml` file ("App-side pins, overrides, and prompt-ID mappings") and the RUNTIME domain depends on CONTRACTS to define its JSON validation schema.
- **Impact**: Unlocks the RUNTIME domain's ability to implement the minimal consumption runtime and resolver, as they will have a formal schema to validate consumption manifests against.

#### 2. File Inventory
- **Create**: `promptops/schemas/consumption-manifest.schema.json` (JSON Schema for the consumption manifest)
- **Modify**: None
- **Read-Only**: `README.md`, `promptops/schemas/prompt-spec.schema.json`

#### 3. Implementation Spec
- **Schema Architecture**:
  - Format: JSON Schema (draft 2020-12)
  - Type: `object`
  - Required Fields: `version` (string, e.g., "1.0.0"), `prompts` (object mapping local names to resolution configurations).
  - Optional Fields: `defaults` (object for global fallbacks, like default model or provider).
  - The `prompts` object:
    - Keys are the application's local, friendly names for prompts.
    - Values are objects that specify how to resolve the prompt.
    - Required properties for a prompt resolution config: `id` (string, the stable prompt ID).
    - Optional properties for a prompt resolution config: `pin` (string, e.g., a semver or git ref to pin to), `override` (string, path to a local file overriding the prompt), `model` (string, model to use).
- **Content Digest Convention**: The consumption manifest itself is typically not published, but if hashed, it would follow the standard SHA-256 of canonical JSON (using `jq -cSM .` after `yq .` conversion).
- **Pseudo-Code**:
  - Load the consumption manifest (e.g., `consumption.yaml`).
  - Convert YAML to JSON.
  - Load the `consumption-manifest.schema.json`.
  - Validate the JSON against the schema.
  - Fail if required fields (`version`, `prompts`) are missing or if types are incorrect.
- **Public Contract Changes**: Exports the `https://apastra.com/schemas/promptops/consumption-manifest.schema.json` schema ID.
- **Dependencies**: None. (RUNTIME depends on this to complete its resolver implementation).

#### 4. Test Plan
- **Verification**: `npx ajv-cli validate -s promptops/schemas/consumption-manifest.schema.json -d test-fixtures/valid-consumption.yaml --spec=draft2020 --strict=false`
- **Success Criteria**: The `ajv` command exits with code 0, indicating the schema correctly validates a well-formed consumption manifest.
- **Edge Cases**: Malformed inputs missing `version` or `prompts`, or where `prompts` contains items lacking an `id`, should be rejected with validation errors.