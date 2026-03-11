#### 1. Context & Goal
- **Objective**: Implement schema validation for resolved prompt specifications against `promptops/schemas/prompt-spec.schema.json`.
- **Trigger**: The Minimal Runtime section in README.md requires that resolved outputs conform to expected contracts. Currently, `resolve()` returns dictionaries or raw strings without validating them against the `prompt-spec.schema.json` defined by CONTRACTS.
- **Impact**: Guarantees that downstream consumers (EVALUATION harnesses, applications) always receive valid, well-formed prompt objects (with `id`, `variables`, and `template`) regardless of the resolution source (local, git, packaged).

#### 2. File Inventory
- **Create**: None
- **Modify**: `promptops/runtime/resolve.py`
- **Read-Only**: `promptops/schemas/prompt-spec.schema.json`, `README.md`

#### 3. Implementation Spec
- **Resolver Architecture**: In `resolve()`, after `ResolverChain().resolve()` returns the prompt data, it must be validated before returning the template and metadata. If validation fails, a `RuntimeError` should be raised. Since `ajv-cli` requires file inputs, dump the data to a temporary JSON file, validate via subprocess, and clean up.
- **Manifest Format**: N/A
- **Pseudo-Code**:
  ```python
  def resolve(prompt_id, ref_context=None):
      # existing resolution logic...
      prompt_spec = ResolverChain().resolve(prompt_id, manifest)

      if not prompt_spec:
          raise RuntimeError(f"Failed to resolve prompt '{prompt_id}'")

      # Handle legacy string returns temporarily or cast them to a mock valid spec for validation.
      if isinstance(prompt_spec, str):
          prompt_spec = {"id": prompt_id, "variables": {}, "template": prompt_spec}

      # Validation Block
      import tempfile, subprocess, os
      with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as tmp:
          json.dump(prompt_spec, tmp)
          tmp_path = tmp.name

      try:
          schema_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "schemas", "prompt-spec.schema.json"))
          cmd = ["npx", "--yes", "ajv-cli", "validate", "-s", schema_path, "-d", tmp_path, "--spec=draft2020", "--strict=false", "-c", "ajv-formats"]
          result = subprocess.run(cmd, shell=False, capture_output=True, text=True)
          if result.returncode != 0:
              raise RuntimeError(f"Resolved prompt failed schema validation: {result.stderr or result.stdout}")
      finally:
          os.remove(tmp_path)

      # existing digest computation and return logic...
  ```
- **Harness Contract Interface**: N/A
- **Dependencies**: CONTRACTS `promptops/schemas/prompt-spec.schema.json`

#### 4. Test Plan
- **Verification**: `mkdir -p test-fixtures && echo '{"id": "invalid"}' > test-fixtures/bad-prompt.json && echo '{"prompts": {"my-prompt": {"id": "my-prompt", "override": "test-fixtures/bad-prompt.json"}}, "version": "1.0"}' > test-fixtures/manifest.json && python -c "from promptops.runtime.resolve import resolve; resolve('my-prompt', 'test-fixtures/manifest.json')" 2>/dev/null`
- **Success Criteria**: `[ $? -ne 0 ]`
- **Edge Cases**: Valid prompt spec should pass resolution and return successfully.
