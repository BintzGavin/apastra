#### 1. Context & Goal
- **Objective**: Ensure the `resolve()` function validates its resolved prompt specifications against the `promptops/schemas/prompt-spec.schema.json` contract.
- **Trigger**: README.md proposes an architecture that makes prompts behave like disciplined software assets with a declared interface, but the current minimal runtime does not enforce the schema of the resolved prompt.
- **Impact**: Guarantees well-formed outputs and ensures that downstream consumers (EVALUATION harnesses, app-side manifests) can reliably depend on the prompt structure (e.g., variables, output contract) defined in the CONTRACTS domain.

#### 2. File Inventory
- **Create**: None
- **Modify**: `promptops/runtime/resolve.py` to add `ajv-cli` schema validation against `promptops/schemas/prompt-spec.schema.json` after resolving the prompt specification.
- **Read-Only**: `promptops/schemas/prompt-spec.schema.json` to understand the validation target.

#### 3. Implementation Spec
- **Resolver Architecture**: The resolution chain (local → workspace → git ref → packaged artifact) remains identical. The change occurs after a successful resolution to validate the returned object.
- **Manifest Format**: Unchanged.
- **Pseudo-Code**:
  1. Resolve `manifest = load_manifest(ref_context)`.
  2. Resolve `prompt_spec = ResolverChain().resolve(prompt_id, manifest)`.
  3. Format `prompt_spec` into a dictionary if it is a string template.
  4. Write `prompt_spec` to a temporary JSON file.
  5. Run `npx --yes ajv-cli validate` against the `prompt-spec.schema.json` using the temporary file.
  6. If validation fails, raise a `RuntimeError` with the validation output.
  7. Return the template and metadata.
- **Harness Contract Interface**: Not applicable.
- **Dependencies**: `promptops/schemas/prompt-spec.schema.json` (must exist in CONTRACTS).

#### 4. Test Plan
- **Verification**:
  ```bash
  mkdir -p test-fixtures
  cat << 'INNER_EOF' > test-fixtures/invalid-prompt.yaml
  id: invalid-prompt
  # Missing variables and template
  INNER_EOF
  cat << 'INNER_EOF' > test-fixtures/manifest.yaml
  prompts:
    invalid-prompt:
      override: test-fixtures/invalid-prompt.yaml
  version: "1.0"
  INNER_EOF
  cat << 'INNER_EOF' > test-fixtures/test_validation.py
  from promptops.runtime.resolve import resolve
  try:
      resolve('invalid-prompt', 'test-fixtures/manifest.yaml')
      print('Validation missing')
  except RuntimeError as e:
      if 'failed' in str(e).lower() or 'invalid' in str(e).lower():
          print('Validation successful')
      else:
          print(f'Unexpected error: {e}')
  INNER_EOF
  python test-fixtures/test_validation.py
  ```
- **Success Criteria**: The test script prints "Validation successful" or raises a `RuntimeError` indicating schema validation failure when given an invalid prompt spec.
- **Edge Cases**: Valid prompt strings dynamically wrapped in dicts, prompt spec missing required fields like `id` or `variables`, ajv-cli missing from environment.
