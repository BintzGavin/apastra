#### 1. Context & Goal
- **Objective**: Create a `starter-pack.schema.json` schema and its validator for community prompt starter packs.
- **Trigger**: `docs/vision.md` outlines "Expansion 5: Community prompt packs" featuring starter packs that bundle prompts, datasets, and evaluators, installable as a git dependency.
- **Impact**: Enables the structured bundling and distribution of standard AI tasks (like summarization or extraction), bootstrapping the prompt registry ecosystem. Downstream tools can consume these packs to onboard new users.

#### 2. File Inventory
- **Create**:
  - `promptops/schemas/starter-pack.schema.json`
  - `promptops/validators/validate-starter-pack.sh`
- **Modify**: None
- **Read-Only**: None

#### 3. Implementation Spec
- **Schema Architecture**:
  - `id`: Stable identifier (e.g., `starter-packs/summarization`).
  - `name`: Human-readable name.
  - `description`: Overview of what the pack solves.
  - `repository`: Git repository URL containing the pack contents.
  - `prompts`: Array of prompt spec references included.
  - `datasets`: Array of dataset references included.
  - `evaluators`: Array of evaluator references included.
  - `baselines`: Array of pre-built baseline references.
- **Content Digest Convention**: N/A (packs reference content but the starter pack index itself does not strictly require digesting as it's a directory).
- **Pseudo-Code**:
  - `validate-starter-pack.sh`: `ajv validate -s promptops/schemas/starter-pack.schema.json -d <test-fixture>`
- **Public Contract Changes**: Exports `starter-pack.schema.json`.
- **Dependencies**: None.

#### 4. Test Plan
- **Verification**: Run `validate-starter-pack.sh` against a valid mock starter pack JSON.
- **Success Criteria**: `ajv` exits with 0 and prints valid message.
- **Edge Cases**: Missing `id`, `name`, `repository`, or invalid types in arrays.
