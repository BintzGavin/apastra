#### 1. Context & Goal
- **Objective**: Implement semver tag resolution in the GitRefResolver.
- **Trigger**: The README.md promises that Git-first resolution supports pinning by semver tags (e.g., `#semver:<range>`), but `promptops/resolver/git_ref.py` currently only supports exact commit SHAs or exact git tags via `git show`.
- **Impact**: Unlocks dynamic, yet bounded, resolution of prompt packages for app-side manifests, allowing consumers to securely receive non-breaking prompt updates automatically without manually updating the consumption manifest for every patch release.

#### 2. File Inventory
- **Create**: None
- **Modify**: `promptops/resolver/git_ref.py` (Add semver parsing and tag listing logic)
- **Read-Only**: `README.md` (Git-first resolution section)

#### 3. Implementation Spec
- **Resolver Architecture**: The resolver chain (local → workspace → git ref) will remain structurally the same. However, when the `GitRefResolver` receives a `pin` starting with `semver:`, it will not immediately run `git show`. Instead, it will:
  1. Parse the semantic version range.
  2. Execute `git tag --list` to fetch all available local tags.
  3. Filter the tags against the semver range.
  4. Select the highest matching tag.
  5. Execute `git show {selected_tag}:promptops/prompts/{prompt_id}/prompt.yaml` (or `.json`).
  If no tag matches the range, it will raise a `RuntimeError`. For exact SHAs or tags (no `semver:` prefix), it will retain the existing behavior.
- **Manifest Format**: The manifest format remains unchanged. The `pin` field (string) in the consumption manifest will continue to store the ref, but now `semver:^1.0.0` will be a functionally supported value.
- **Pseudo-Code**:
  ```python
  def resolve(self, prompt_id, pin):
      if pin.startswith("semver:"):
          range = pin.replace("semver:", "")
          tags = run_git_command("git tag --list")
          valid_tags = filter_semver_tags(tags, range)
          if not valid_tags:
              raise RuntimeError("No matching semver tag found")
          pin = get_highest_semver(valid_tags)

      # existing logic...
      try git show pin:promptops/prompts/prompt_id/prompt.yaml
      if success return parsed yaml
      try git show pin:promptops/prompts/prompt_id/prompt.json
      if success return parsed json
      raise RuntimeError
  ```
- **Harness Contract Interface**: N/A for this task.
- **Dependencies**: No new CONTRACTS schemas required, relies on existing `consumption-manifest.schema.json`.

#### 4. Test Plan
- **Verification**: Run `python promptops/runtime/cli.py my-prompt --ref semver:^1.0.0` in a repo with `v1.0.0`, `v1.1.0` and `v2.0.0` tags.
- **Success Criteria**: The resolution logic correctly identifies and returns the prompt content from the `v1.1.0` tag, ignoring `v2.0.0`.
- **Edge Cases**: No matching tags in the repository for the given range, Invalid semver string, Shallow clone where tags are not fetched.
