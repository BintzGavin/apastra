#### 1. Context & Goal
- **Objective**: Implement quick eval format resolution in the LocalResolver.
- **Trigger**: `docs/vision.md` mentions "Quick eval mode" where a single file in `promptops/evals/` contains `prompt`, `cases`, and `assertions`. "The agent reads a quick eval file and internally treats it as a prompt spec...". This was implemented for the WorkspaceResolver and GitRefResolver, and parity is required for the LocalResolver.
- **Impact**: Enables rapid iteration smoke tests by parsing a local override path containing a quick eval file (e.g., `promptops/evals/my-eval.yaml`) and returning a valid prompt spec object (`id`, `template`, `variables` inferred from template or empty).

#### 2. File Inventory
- **Create**: None
- **Modify**: `promptops/resolver/local.py`
- **Read-Only**: `promptops/schemas/quick-eval.schema.json`, `docs/vision.md`

#### 3. Implementation Spec
- **Resolver Architecture**: Update `LocalResolver.resolve()` to intercept the returned dictionary from `load_prompt_package(override_path)`. If the returned dictionary has a `prompt` key (and optionally `cases` or `id`), convert it into a `prompt-spec` compatible dictionary: `{"id": prompt_id, "template": data["prompt"], "variables": {}}`.
- **Manifest Format**: N/A
- **Pseudo-Code**:
  ```python
  class LocalResolver:
      def resolve(self, prompt_id, override_path):
          if not os.path.exists(override_path):
              raise FileNotFoundError(f"Local override path not found: {override_path}")

          data = load_prompt_package(override_path)

          # Quick eval resolution
          if data and "prompt" in data:
              return {"id": prompt_id, "template": data["prompt"], "variables": {}}

          return data
  ```
- **Harness Contract Interface**: N/A
- **Dependencies**: CONTRACTS `quick-eval.schema.json`

#### 4. Test Plan
- **Verification**: `mkdir -p promptops/evals && echo -e 'id: my-local-eval\nprompt: "Local quick prompt"' > promptops/evals/my-local-eval.yaml && python -c "from promptops.resolver.local import LocalResolver; print(LocalResolver().resolve('my-local-eval', 'promptops/evals/my-local-eval.yaml'))"`
- **Success Criteria**: Returns `{'id': 'my-local-eval', 'template': 'Local quick prompt', 'variables': {}}`.
- **Edge Cases**: Regular local prompts still resolve correctly; handles missing file errors correctly.
