#### 1. Context & Goal
- **Objective**: Fix shallow clone failures when resolving remote git URLs by commit SHA in the `GitRefResolver`.
- **Trigger**: The docs specify "Resolve by semver/tag/SHA-like ref". The current GitRefResolver implementation for remote git URLs (`git+https://...#<ref>`) attempts to use `git clone --depth 1 --branch <ref>`, which fails when the ref is a commit SHA rather than a branch or tag name.
- **Impact**: This bug prevents developers from securely pinning dependencies by commit SHA when consuming remote prompt packages via the consumption manifest, violating the core deterministic Git-first resolution requirements.

#### 2. File Inventory
- **Create**: None
- **Modify**: `promptops/resolver/git_ref.py`
- **Read-Only**: `.jules/prompts/planning-runtime.md`, `docs/vision.md`

#### 3. Implementation Spec
- **Resolver Architecture**: When fetching a remote repository in `GitRefResolver` (via `git+` URI), if the `git archive` fallback path is hit, the `git clone` command fails on SHAs. The logic must be updated to:
  1. perform a basic `git clone` into the temporary directory (without the `--depth 1 --branch <ref>` flags which break on SHAs).
  2. then `git checkout <ref>` inside the cloned repository to switch to the exact commit SHA, branch, or tag.
- **Manifest Format**: Unchanged.
- **Pseudo-Code**:
  ```python
  # Instead of:
  # clone_cmd = ["git", "clone", "--depth", "1", "--branch", ref_part, url_part, temp_dir]
  # result = subprocess.run(clone_cmd, ...)

  # Use:
  clone_cmd = ["git", "clone", url_part, temp_dir]
  result = subprocess.run(clone_cmd, capture_output=True, check=False)
  if result.returncode != 0:
      raise RuntimeError(f"Failed to fetch remote git repo: {result.stderr.decode('utf-8')}")

  checkout_cmd = ["git", "-C", temp_dir, "checkout", ref_part]
  checkout_result = subprocess.run(checkout_cmd, capture_output=True, check=False)
  if checkout_result.returncode != 0:
      raise RuntimeError(f"Failed to checkout ref in remote git repo: {checkout_result.stderr.decode('utf-8')}")
  ```
- **Harness Contract Interface**: Unchanged.
- **Dependencies**: None. No new CONTRACTS schemas are required.

#### 4. Test Plan
- **Verification**:
  1. Create a local test repository, add a prompt, and commit it.
  2. Record the commit SHA.
  3. Create a consumption manifest mapping a prompt to the local repo URL with `#<SHA>`.
  4. Run `python -c "from promptops.resolver.git_ref import GitRefResolver; print(GitRefResolver().resolve('my-prompt', 'git+file://<test_repo_path>#<SHA>'))"`
- **Success Criteria**: The resolver correctly fetches and parses the prompt package from the remote git URL pinned by the commit SHA.
- **Edge Cases**: Ensure the logic still successfully resolves branch names and tag names as refs, alongside SHAs.
