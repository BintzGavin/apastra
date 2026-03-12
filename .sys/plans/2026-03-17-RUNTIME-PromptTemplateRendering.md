#### 1. Context & Goal
- **Objective**: Implement template rendering in the minimal runtime's resolve function.
- **Trigger**: `README.md` defines the minimal runtime core function as `resolve(promptId, ref) → rendered prompt + metadata` and the build plan specifies `resolve prompt ID → render template → return structured prompt + metadata`. Currently, `promptops/runtime/resolve.py` only returns the raw template and does not perform any variable injection or templating.
- **Impact**: Unlocks EVALUATION harnesses and downstream app-side consumers to pass dynamic variables and receive a fully rendered prompt ready for provider SDKs.

#### 2. File Inventory
- **Create**: `promptops/runtime/render.py` (New module to handle template substitution)
- **Modify**: `promptops/runtime/resolve.py` (Update `resolve()` to accept a `variables` dict and return the rendered prompt instead of the raw template)
- **Read-Only**: `promptops/schemas/prompt-spec.schema.json`

#### 3. Implementation Spec
- **Resolver Architecture**: The resolution chain remains the same (local → workspace → git ref → packaged). After the prompt spec is resolved and validated against the schema, the runtime must merge the provided `variables` dict with the prompt spec's `template`.
- **Manifest Format**: No changes to the manifest format.
- **Pseudo-Code**:
  ```python
  def resolve(prompt_id, ref_context=None, variables=None):
      # ... existing resolution and validation logic ...
      prompt_spec = ResolverChain().resolve(prompt_id, manifest)
      # validate schema
      rendered_prompt = render_template(prompt_spec.get('template'), variables or {})
      return rendered_prompt, metadata
  ```
- **Harness Contract Interface**: Harness adapters will need to pass variables from datasets into this render function.
- **Dependencies**: `promptops/schemas/prompt-spec.schema.json` must exist (it does).

#### 4. Test Plan
- **Verification**: Run a python script that calls `resolve('my-prompt', ref_context, variables={'name': 'Alice'})` where the template contains a `{{name}}` or similar placeholder, and verify the placeholder is replaced.
- **Success Criteria**: The output of `resolve()` contains the string with variables successfully substituted.
- **Edge Cases**: Missing variables, extra variables, template as a string vs template as an array of message objects.
