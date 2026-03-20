#### 1. Context & Goal
- **Objective**: Extend GitRefResolver to support remote git URLs (e.g., `git+https://...#<ref>`) enabling the separate-repo consumption model.
- **Trigger**: The vision document explicitly lists `git+...#<sha>` as a supported pinning surface in consumption manifests for the Git ref packaging mode, but the current `GitRefResolver` only supports local git refs via `git show`.
- **Impact**: This unlocks the separate-repo consumption topology, allowing downstream applications to consume prompt packages from dedicated prompt repositories without requiring those repos to publish formal release assets.

#### 2. File Inventory
- **Create**: None
- **Modify**: `promptops/resolver/git_ref.py` (Add logic to parse remote git URLs, perform sparse checkouts or remote archive fetches, and read the prompt package).
- **Read-Only**: `docs/vision.md` (Repo topology model and Git-first resolution sections), `README.md` (Consumption section).

#### 3. Implementation Spec
- **Resolver Architecture**:
  - The `GitRefResolver.resolve()` method will be updated to detect if the `pin` starts with `git+`.
  - If a remote URL is detected, it will extract the repository URL and the reference (SHA or tag) after the `#` symbol.
  - To avoid full repository clones, the resolver will use `git archive --remote=<URL> <ref> promptops/prompts/<prompt_id>.yaml | tar -x` (or similar Git-native remote extraction techniques) to fetch only the required files into a temporary directory.
  - It will then load the prompt package from the temporary directory using the same hierarchical fallback logic (flat yaml, flat json, directory structure) as local refs.
  - The in-memory cache will still apply using the `(prompt_id, pin)` tuple as the key.
- **Manifest Format**: The manifest format already supports arbitrary string pins. No changes required to the `consumption-manifest.schema.json`. Examples of valid pins will now include `git+https://github.com/org/prompt-repo.git#v1.0.0` or `git+ssh://git@github.com/org/repo.git#abcdef123`.
- **Pseudo-Code**:
  ```python
  def resolve(self, prompt_id, pin):
      cache_key = (prompt_id, pin)
      if cache_key in self.cache: return self.cache[cache_key]

      if pin.startswith('git+'):
          # Parse URL and ref
          url_part, ref_part = pin[4:].split('#')

          # Use git archive to extract specific files to a temp directory
          # Fallback to shallow clone if git archive is disabled on the remote

          # Read files from temp directory using existing fallback logic
          # (promptops/prompts/{id}.yaml, .json, etc.)

          # Cache and return result
      else:
          # Existing local git show logic
  ```
- **Harness Contract Interface**: No changes required.
- **Dependencies**: No new CONTRACTS schemas required.

#### 4. Test Plan
- **Verification**: Run `resolve('my-prompt', 'git+https://github.com/example/repo.git#v1.0.0')` using the reference CLI and confirm the output matches the expected fixture from that remote repository.
- **Success Criteria**: The resolver successfully fetches and parses the prompt package from a remote git repository without requiring a full local clone.
- **Edge Cases**: Network failures, repository not found, authentication failures (private repos), ref not found, prompt file missing in the remote ref, remote server disables `git archive`.
