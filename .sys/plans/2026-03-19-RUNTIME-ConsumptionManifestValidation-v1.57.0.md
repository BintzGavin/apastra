#### 1. Context & Goal
- **Objective**: Validate the consumption manifest format against its CONTRACTS schema.
- **Trigger**: The docs/vision.md and README.md specify that the consumption manifest "Must validate against CONTRACTS schema for manifests" (priority gap #1).
- **Impact**: Ensures that applications only consume correctly formatted manifests, unlocking robust validation for downstream systems.

#### 2. File Inventory
- **Create**: `promptops/manifests/consumption.py` (to define manifest loading and validation logic)
- **Modify**: `promptops/resolver/chain.py` (to invoke validation before evaluating rules)
- **Read-Only**: `promptops/schemas/consumption-manifest.schema.json`, `docs/vision.md`

#### 3. Implementation Spec
- **Resolver Architecture**: The resolver chain receives the manifest object. Before parsing its rules, the manifest object is validated against the defined `promptops/schemas/consumption-manifest.schema.json`. If it fails validation, an explicit error detailing the failed rules is raised. If it passes, the resolver proceeds to evaluate local override -> workspace -> git ref.
- **Manifest Format**: Follows the `promptops/schemas/consumption-manifest.schema.json` schema, which dictates the prompt mapping structure, stable prompt IDs, and pin/override/model fields.
- **Pseudo-Code**:
  ```python
  def validate_manifest(manifest_content):
      schema = load_schema("promptops/schemas/consumption-manifest.schema.json")
      validate(manifest_content, schema)  # Raises exception on failure
      return parse_yaml(manifest_content)
  ```
- **Harness Contract Interface**: None
- **Dependencies**: Depends on `promptops/schemas/consumption-manifest.schema.json` (already exists).

#### 4. Test Plan
- **Verification**: Run a minimal python script `test_validate.py` that imports the newly created validation logic and attempts to parse an invalid manifest (e.g. missing `version`), expecting an exception.
- **Success Criteria**: A validation exception is thrown indicating that the `version` field is required.
- **Edge Cases**: Missing required fields, invalid types (e.g., array instead of string for `pin`), malformed YAML syntax.