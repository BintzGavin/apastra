#### 1. Context & Goal
- **Objective**: Fix the `GitRefResolver` to correctly handle explicit commit SHAs when resolving remote git URLs.
- **Trigger**: The vision document explicitly outlines the need for remote git URL resolution, specifying "Local overrides and git-ref pins (commit SHA or tag, optionally semver) are first-class". Currently, `git clone --depth 1 --branch <ref>` fails for commit SHAs because most git servers do not allow fetching a specific SHA without a full clone or fetch.
- **Impact**: Enables robust resolution of remote git references via commit SHAs across different app-side manifest configurations.

#### 2. File Inventory
- **Create**: None
- **Modify**: `promptops/resolver/git_ref.py` - Update fallback logic in `resolve()` for remote git references to handle commit SHAs.
- **Read-Only**: `docs/vision.md`

#### 3. Implementation Spec
- **Resolver Architecture**: In `GitRefResolver`, detect if a ref looks like a commit SHA (e.g., matching a 40-character hex string). If it is a SHA, fallback from `git archive` to a full `git clone` without `--depth 1 --branch`, then execute a `git checkout <sha>` within the cloned temp directory. If it's a branch or tag, continue using the shallow clone strategy.
- **Manifest Format**: Unchanged.
- **Pseudo-Code**:
  ```python
  # inside resolve()
  if archive_p.returncode != 0:
      # fallback to clone
      is_sha = len(ref_part) == 40 and all(c in '0123456789abcdefABCDEF' for c in ref_part)
      if is_sha:
          subprocess.run(["git", "clone", url_part, temp_dir], check=True)
          subprocess.run(["git", "-C", temp_dir, "checkout", ref_part], check=True)
      else:
          subprocess.run(["git", "clone", "--depth", "1", "--branch", ref_part, url_part, temp_dir], check=True)
  ```
- **Harness Contract Interface**: Unchanged.
- **Dependencies**: None.

#### 4. Test Plan
- **Verification**: Run `python3 promptops/cli.py resolve my-prompt --pin git+https://github.com/my-org/prompts.git#<commit_sha>`
- **Success Criteria**: The CLI correctly clones, checks out the SHA, and resolves the prompt without throwing a `git clone` failure error.
- **Edge Cases**: Ensure the logic still correctly falls back to `--depth 1 --branch <ref>` for tags or branch names.
