#### 1. Context & Goal
- **Objective**: Design the git ref resolution step in the resolver chain to support pinning by commit SHA or tag.
- **Trigger**: The README.md requires git ref pins (commit SHA, tag) as a first-class resolution mechanism, but `promptops/resolver/chain.py` throws NotImplementedError.
- **Impact**: Enables consuming apps to pin prompt versions to specific commits or tags without publishing artifacts, ensuring reproducible prompts across environments.

#### 2. File Inventory
- **Create**:
  - `promptops/resolver/[new_git_resolver_file].py`: New file to implement Git ref resolution logic.
- **Modify**:
  - `promptops/resolver/chain.py`: Update the fallback chain to use the Git resolver when `pin` is specified and workspace resolution is skipped/fails.
- **Read-Only**:
  - `README.md` (Git-first resolution section)
  - `promptops/schemas/consumption-manifest.schema.json`

#### 3. Implementation Spec
- **Resolver Architecture**: The git resolver must take a repo context and a git ref (`pin` string from manifest). It should pull/fetch the ref, locate the `prompt_id` within the `promptops/` workspace at that commit, and return the resolved content. If the ref is not found or not accessible, fail gracefully.
- **Manifest Format**: Uses the `pin` field defined in `consumption-manifest.schema.json`, which expects a string (commit SHA or tag).
- **Pseudo-Code**:
  ```python
  # def [resolve_function_name](prompt_id, pin_ref, repo_url=None):
      # if repo_url not given, assume current repo
      # shell out to git or use a git library to fetch the tree at pin_ref
      # read promptops/valid-workspace-prompt.yaml at that commit (for matching ID)
      # return parsed prompt data
  ```
- **Harness Contract Interface**: None directly changed, but execution environments will need git access.
- **Dependencies**: Depends on the existing `promptops/schemas/consumption-manifest.schema.json` schema.

#### 4. Test Plan
- **Verification**: `python3 -c "from promptops.resolver.chain import ResolverChain; class Manifest: get_rules = lambda self, p: {'pin': 'HEAD'}; ResolverChain().resolve('mock_id', Manifest())"`
- **Success Criteria**: `echo 'git resolution successful'`
- **Edge Cases**: `echo 'test shallow clone failure handling'`
