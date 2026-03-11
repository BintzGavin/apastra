#### 1. Context & Goal
- **Objective**: Define the minimal `resolve()` function interface for the prompt runtime.
- **Trigger**: The README.md specifies a minimal runtime function `resolve(promptId, ref) → rendered prompt + metadata` that needs its interface designed.
- **Impact**: Unlocks the ability for EVALUATION harnesses and downstream apps to consume prompts via a stable, stateless compute contract.

#### 2. File Inventory
- **Create**: `promptops/runtime/resolve.py` (Implementation of the minimal runtime interface)
- **Modify**: `promptops/resolver/chain.py` (Update `ResolverChain` to fit inside the `resolve` flow)
- **Read-Only**: `README.md` (Minimal Runtime section), `promptops/schemas/consumption-manifest.schema.json`

#### 3. Implementation Spec
- **Resolver Architecture**: The `resolve()` function acts as the public entry point. It accepts a `prompt_id` and an optional `ref` (or context object). It uses the `ResolverChain` to find the prompt package (checking local override -> workspace -> git ref -> fallback). Once resolved, it reads the prompt spec and returns a tuple/dict containing the raw/rendered prompt and metadata (prompt digest, dataset digest, harness version, model IDs).
- **Manifest Format**: Uses existing consumption manifest format (`override` for local, `pin` for git ref).
- **Pseudo-Code**:
  ```python
  def resolve(prompt_id, ref_context=None):
      manifest = load_manifest(ref_context)
      prompt_path = ResolverChain().resolve(prompt_id, manifest)
      prompt_spec = read_yaml_or_json(prompt_path)
      metadata = {
          "prompt_digest": compute_digest(prompt_spec),
      }
      return prompt_spec.get('template'), metadata
  ```
- **Harness Contract Interface**: Input is `run_request.json` with a revision ref. The harness calls `resolve()` to get the prompt package and evaluates it, then emits `run_manifest.json` and `scorecard.json`.
- **Dependencies**: Requires `promptops/schemas/consumption-manifest.schema.json` (exists) and `promptops/schemas/prompt-spec.schema.json` (exists).

#### 4. Test Plan
- **Verification**: Exact command: `echo '{"id":"test-prompt","template":"hello"}' > test-fixtures/test-prompt.json; python3 -c "from promptops.runtime.resolve import resolve; resolve('test-prompt', 'test-fixtures/test-prompt.json')"`
- **Success Criteria**: `python3 -c "from promptops.runtime.resolve import resolve; resolve('test-prompt', 'test-fixtures/test-prompt.json')"; [ $? -eq 0 ]`
- **Edge Cases**: `python3 -c "from promptops.runtime.resolve import resolve; resolve('missing-prompt', 'test-fixtures/test-prompt.json')" 2>/dev/null; [ $? -ne 0 ]`