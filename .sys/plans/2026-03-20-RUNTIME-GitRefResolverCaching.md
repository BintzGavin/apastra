#### 1. Context & Goal
- **Objective**: Implement caching in `GitRefResolver` to reduce duplicate `git show` subprocess calls for identical prompt resolutions within the same process.
- **Trigger**: The vision document emphasizes low-friction and reproducible resolution. The `GitRefResolver` currently executes `git show` subprocesses via `subprocess.run` on every resolution, creating unnecessary overhead when the same prompt ID and Git ref are repeatedly resolved.
- **Impact**: Improves performance for consumption manifests or downstream execution suites that resolve the same remote prompt multiple times.

#### 2. File Inventory
- **Create**: None
- **Modify**: `promptops/resolver/git_ref.py` (Add a `self.cache` dictionary to `GitRefResolver` and bypass `git show` logic on cache hits based on `(prompt_id, pin)` tuples).
- **Read-Only**: `docs/vision.md` and `README.md` (Checked Git-first consumption performance implications).

#### 3. Implementation Spec
- **Resolver Architecture**: The resolution chain maintains its `GitRefResolver` step, but internally caches `(prompt_id, pin)` tuples to avoid duplicate `subprocess.run(["git", "show", ...])` calls.
- **Manifest Format**: Unchanged.
- **Pseudo-Code**:
  ```python
  class GitRefResolver:
      def __init__(self):
          self.cache = {}

      def resolve(self, prompt_id, pin):
          cache_key = (prompt_id, pin)
          if cache_key in self.cache:
              return self.cache[cache_key]

          # ... perform existing git show logic via subprocess.run ...
          # if successful, self.cache[cache_key] = result
          return result
  ```
- **Harness Contract Interface**: Unchanged.
- **Dependencies**: No new CONTRACTS schemas required.

#### 4. Test Plan
- **Verification**: Instantiate `GitRefResolver`, call `resolve('summarize-v1', 'HEAD')` twice, and assert that `subprocess.run` is called fewer times or that the execution time of the second call is significantly reduced.
- **Success Criteria**: The second call returns identical results without invoking `git show`.
- **Edge Cases**: Semver range resolution must still return the correct object; invalid refs must still fail predictably.
