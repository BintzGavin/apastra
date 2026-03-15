#### 1. Context & Goal
- **Objective**: Implement local alias mapping to stable IDs and model metadata propagation in the resolver chain.
- **Trigger**: The `docs/vision.md` outlines that the consumption manifest enables "mappings from prompt IDs to usage" (meaning an app can use a local name that maps to a stable `id`). Additionally, the "Minimal Runtime" section promises that `resolve()` returns metadata including "model IDs".
- **Impact**: Enables downstream applications to request a local alias (e.g., `summarize-latest`) that maps to a stable ID (e.g., `my-app/summarize-v1`) without changing application code. Also provides evaluation harnesses with the required model configuration.

#### 2. File Inventory
- **Create**: None.
- **Modify**: `promptops/resolver/chain.py` (to pass mapped ID to underlying resolvers)
- **Modify**: `promptops/runtime/resolve.py` (to extract and include `model` from manifest in returned metadata)
- **Read-Only**: `promptops/schemas/consumption-manifest.schema.json`, `docs/vision.md`

#### 3. Implementation Spec
- **Resolver Architecture**: In `ResolverChain.resolve(self, prompt_id, manifest)`, the actual prompt ID requested from the fallback resolvers (Workspace, GitRef, Packaged) should be the `id` specified in the manifest rules, not necessarily the `prompt_id` key requested by the app. `target_id = rules.get('id', prompt_id)`.
- **Manifest Format**: The consumption manifest supports a local mapping under `prompts`, e.g., `summarize: { id: summarize-v1, model: gpt-4 }`. The schema already permits `id` and `model` fields inside the `prompts` object values, and a `defaults.model` fallback.
- **Pseudo-Code**:
  In `promptops/resolver/chain.py`:
  ```python
  class ResolverChain:
      def resolve(self, prompt_id, manifest):
          rules = manifest.get_rules(prompt_id) if hasattr(manifest, 'get_rules') else {}
          target_id = rules.get('id', prompt_id)

          if rules and 'override' in rules:
              return LocalResolver().resolve(target_id, rules['override'])

          workspace_result = WorkspaceResolver().resolve(target_id)
          # ...
          if rules and 'pin' in rules:
              pin = rules['pin']
              return GitRefResolver().resolve(target_id, pin)
  ```
  In `promptops/runtime/resolve.py`:
  ```python
  def resolve(prompt_id, ref_context=None, variables=None):
      manifest = load_manifest(ref_context)
      # ...
      rules = manifest.get_rules(prompt_id) if hasattr(manifest, 'get_rules') else {}
      defaults = manifest.data.get('defaults', {}) if hasattr(manifest, 'data') and isinstance(manifest.data, dict) else {}
      model_id = rules.get('model', defaults.get('model'))

      metadata = {
          "prompt_digest": compute_digest_from_dict(prompt_spec),
      }
      if model_id:
          metadata["model"] = model_id
  ```
- **Harness Contract Interface**: N/A
- **Dependencies**: Relies on existing CONTRACTS consumption-manifest.schema.json structure.

#### 4. Test Plan
- **Verification**: `mkdir -p test-evals && echo 'version: "1.0"\ndefaults:\n  model: gpt-3.5-turbo\nprompts:\n  my-alias:\n    id: summarize-v1\n    model: gpt-4' > test-evals/manifest.yaml && python -c "from promptops.runtime.resolve import resolve; print(resolve('my-alias', 'test-evals/manifest.yaml'))"`
- **Success Criteria**: Returns the template from `summarize-v1` and metadata containing `{'model': 'gpt-4'}`.
- **Edge Cases**: Missing `id` in manifest mapping correctly defaults to the requested `prompt_id`. Missing `model` in specific prompt falls back to `defaults.model`.