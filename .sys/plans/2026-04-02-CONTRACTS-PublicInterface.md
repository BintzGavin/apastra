#### 1. Context & Goal
- **Objective**: Add `public_interface` schema enforcement to `prompt-package.schema.json` to require explicit API declaration for versioned packages.
- **Trigger**: The vision document (`docs/vision.md`) states: "SemVer is supported when (and only when) the prompt package declares a public interface. SemVer explicitly requires that software declare a public API." and "For prompt packages, the 'public API' should mean: prompt ID, variables schema, output contract/schema, and (if relevant) tool schema/contract." This rule is currently missing from `promptops/schemas/prompt-package.schema.json`.
- **Impact**: This unlocks formal Semantic Versioning for prompt packages by guaranteeing that any package claiming a version explicitly declares the interface it versions, a core requirement for reliable distribution.

#### 2. File Inventory
- **Create**: []
- **Modify**:
  - `promptops/schemas/prompt-package.schema.json`
- **Read-Only**: []

#### 3. Implementation Spec
- **Schema Architecture**:
  - Add `public_interface` to properties of `prompt-package.schema.json`.
  - `public_interface` is an object.
  - `public_interface` contains: `prompt_id` (string), `variables_schema` (object), `output_schema` (object), and `tool_contract` (object).
  - At minimum, `prompt_id` and `variables_schema` are required within `public_interface`.
  - Add `dependentRequired` property to the root of the schema: `"version": ["public_interface"]`.
- **Validator Logic**:
  - `promptops/validators/validate-prompt-package.sh` requires no changes as the script passes validation directly to `ajv-cli`, which handles `dependentRequired` constraints automatically.
- **Dependencies**: None.

#### 4. Test Plan
- **Verification**: Run `promptops/validators/validate-prompt-package.sh test_package.json` against custom test fixtures.
- **Success Criteria**: A versioned package without `public_interface` is rejected. A versioned package with `public_interface` passes. An unversioned package without `public_interface` passes.
- **Edge Cases**: Validation correctly processes `tool_contract` and `output_schema` as optional fields within the public interface.
