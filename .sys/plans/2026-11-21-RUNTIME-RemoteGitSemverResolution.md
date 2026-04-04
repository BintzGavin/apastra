#### 1. Context & Goal
- **Objective**: Implement spec to fetch tags from remote repositories using `git ls-remote --tags` and resolve semver ranges.
- **Trigger**: The vision states "Apps can pin prompts by commit SHA, tag, or semver", but remote git URLs with `semver:` prefixes fail.
- **Impact**: Enables EVALUATION harnesses and app-side manifests to reliably consume prompts securely and precisely from remote repositories.

#### 2. File Inventory
- **Create**: []
- **Modify**: [promptops/resolver/git_ref.py to implement remote git tag fetching and semver resolution]
- **Read-Only**: []

#### 3. Implementation Spec
- **Resolver Architecture**: Extends `GitRefResolver.resolve` to handle `semver:` resolution remotely. Fetches tags from remote using `git ls-remote --tags`, validates against semver range, then delegates to `git archive` or `git clone` checkout fallback with the resolved specific tag.
- **Manifest Format**: Uses consumption manifest schema where `pin` can be a remote git url with a semver prefix.
- **Pseudo-Code**:
  1. Extract remote url and ref range.
  2. Call `subprocess.run` with `["git", "ls-remote", "--tags", url]`.
  3. Parse tags from output and filter using `match_semver`.
  4. Select the highest version matching tag.
  5. Use the selected tag for subsequent git operations.
- **Harness Contract Interface**: N/A
- **Dependencies**: None.

#### 4. Test Plan
- **Verification**: Run `resolve('my-prompt', 'git+https://github.com/org/repo.git#semver:^1.0.0')` and confirm resolved correctly against remote repo.
- **Success Criteria**: Correct prompt metadata and content rendered.
- **Edge Cases**: No matching tag found, missing tag ref format from `ls-remote`.
