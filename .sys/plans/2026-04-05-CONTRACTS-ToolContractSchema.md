#### 1. Context & Goal
- **Objective**: Add `tool_contract` as an optional property to the `prompt-spec.schema.json` to define expected tool calling schemas.
- **Trigger**: `docs/vision.md` explicitly defines the public API for a prompt package as: "prompt ID, variables schema, output contract/schema, and (if relevant) tool schema/contract". The current `prompt-spec.schema.json` lacks a way to define tool schemas/contracts.
- **Impact**: This change unlocks the ability for prompts to define the structure and types of tools they expect to be available, aligning the schema fully with the vision document's requirements.

#### 2. File Inventory
- **Create**: None.
- **Modify**: `promptops/schemas/prompt-spec.schema.json`.
- **Read-Only**: `docs/vision.md`.

#### 3. Implementation Spec
- **Schema Architecture**: Add a new optional property `tool_contract` of type `object` to the `properties` definition in `promptops/schemas/prompt-spec.schema.json`.
- **Content Digest Convention**: N/A
- **Pseudo-Code**:
  - Update the `properties` object in the `prompt-spec.schema.json` file to include `"tool_contract": { "type": "object", "description": "JSON Schema defining the expected tool calling structure and available tools." }`.
- **Public Contract Changes**: The `prompt-spec.schema.json` will allow `tool_contract` as a valid property.
- **Dependencies**: None.

#### 4. Test Plan
- **Verification**: Run `cat promptops/schemas/prompt-spec.schema.json | grep '"tool_contract"'` to verify the new property is added to the schema.
- **Success Criteria**: The output includes the `"tool_contract"` property.
- **Edge Cases**: Ensure existing tests for valid prompt specs still pass.