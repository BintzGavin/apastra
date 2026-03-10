#### 1. Context & Goal
- **Objective**: Design the local override resolution phase of the resolver chain to allow developers to use local prompt paths without publishing.
- **Trigger**: The README.md promises a local override mechanism ("local override for development: developer uses local path without publishing"), but `promptops/resolver/` is empty.
- **Impact**: Unlocks rapid local development. Developers can test prompt changes locally with their application without needing to commit, tag, or push to a remote repository. It serves as the highest-precedence fallback in the `resolve()` chain.

#### 2. File Inventory
- **Create**: `promptops/resolver/local.py` (or equivalent file for local resolution logic), `promptops/resolver/chain.py` (entry point for the resolver)
- **Modify**: None
- **Read-Only**: `README.md` (Git-first consumption, Local override), `promptops/manifests/consumption-example.yaml` (once implemented by executor)

#### 3. Implementation Spec
- **Resolver Architecture**: The local resolver is the first step in the resolution chain. When a prompt ID is requested, the resolver first checks the consumption manifest for a `local_override` rule for that ID. If it exists, it immediately returns the prompt package from that absolute or relative path, bypassing workspace and git ref resolution.
- **Manifest Format**: Relies on the `local_override` field defined in the Consumption Manifest.
- **Pseudo-Code**:
  ```python
  # promptops/resolver/local.py
  import os

  class LocalResolver:
      def resolve(self, prompt_id, override_path):
          """Resolves a prompt package from a local path."""
          if not os.path.exists(override_path):
              raise FileNotFoundError(f"Local override path not found: {override_path}")

          # Return the parsed prompt spec/package from the local path
          return load_prompt_package(override_path)

  # promptops/resolver/chain.py
  class ResolverChain:
      def resolve(self, prompt_id, manifest):
          rules = manifest.get_rules(prompt_id)
          if rules and rules.local_override:
              return LocalResolver().resolve(prompt_id, rules.local_override)
          # ... fallback to workspace ...
  ```
- **Harness Contract Interface**: N/A for this task.
- **Dependencies**: Depends on the CONTRACTS domain implementing `consumption-manifest.schema.json` so the manifest format is standardized.

#### 4. Test Plan
- **Verification**: Run `resolve('my-prompt')` with a manifest that defines `local_override: ./test-fixtures/my-prompt/` and verify the output matches the fixture exactly.
- **Success Criteria**: The resolver correctly loads the prompt from the specified local path, ignoring any git or workspace pins that might also be present in the rules (verifying precedence).
- **Edge Cases**:
  - `local_override` path does not exist (should raise specific error).
  - Invalid prompt package at the local path.
  - Relative paths vs absolute paths handling.
