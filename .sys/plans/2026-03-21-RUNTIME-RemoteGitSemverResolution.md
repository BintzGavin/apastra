#### 1. Context & Goal
- **Objective**: Implement explicit support for semver resolution for remote git URLs in `GitRefResolver`.
- **Trigger**: `docs/vision.md` explicitly states: "Apps can pin prompts by commit SHA, tag, or semver". However, while `semver:` prefixes work locally, remote git URLs (`git+https://...#semver:^1.2.0`) currently fail because the remote fetch logic does not resolve the semver range to a specific tag before fetching.
- **Impact**: Enables downstream consumers to use semver ranges with separate-repo remote git consumption, making cross-repo updates much easier and matching standard package manager behaviors (like npm).

#### 2. File Inventory
- **Create**: None
- **Modify**: `promptops/resolver/git_ref.py`
- **Read-Only**: `docs/vision.md`, `promptops/schemas/consumption-manifest.schema.json`

#### 3. Implementation Spec
- **Resolver Architecture**: In `GitRefResolver.resolve`, when `pin.startswith('git+')` and the `ref_part` starts with `semver:`, we must use `git ls-remote --tags <url>` to fetch remote tags, parse them, run them through `match_semver`, and resolve to the highest matching tag before proceeding with `git archive` or `git clone`.
- **Manifest Format**: No manifest changes required.
- **Pseudo-Code**:
  ```python
  if pin.startswith('git+'):
      url_part, ref_part = pin[4:].split('#', 1)
      if ref_part.startswith('semver:'):
          range_str = ref_part.replace('semver:', '')
          # subprocess run git ls-remote --tags <url_part>
          # parse stdout to get tags, strip refs/tags/ and ^{}
          # valid_tags = [t for t in tags if match_semver(t, range_str)]
          # valid_tags.sort(...)
          # ref_part = valid_tags[0]
      # Continue with archive / clone logic using ref_part
  ```
- **Harness Contract Interface**: Unchanged.
- **Dependencies**: None.

#### 4. Test Plan
- **Verification**: `python3 -c "from promptops.resolver.git_ref import GitRefResolver; print(GitRefResolver().resolve('some-prompt', 'git+https://github.com/some/repo#semver:^1.0.0'))"` (using a real or mock git repo with tags).
- **Success Criteria**: The resolver successfully fetches the highest tag matching the semver range from the remote repository and resolves the prompt.
- **Edge Cases**: No tags match the semver range, invalid semver range, unreachable remote repository.
