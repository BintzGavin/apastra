#### 1. Context & Goal
- **Objective**: Implement caching in the `WorkspaceResolver` to reduce disk reads during repeated prompt resolutions.
- **Trigger**: Repeated workspace resolutions currently read from disk each time, causing potential bottlenecks as mentioned in the `LocalResolverCaching` task but unaddressed for workspace paths.
- **Impact**: Improves the performance of resolution when resolving from the workspace, impacting any consumers relying on workspace resolution (e.g. `apastra-eval` loops).

#### 2. File Inventory
- **Create**: None
- **Modify**: `promptops/resolver/workspace.py` (Specifies caching logic for workspace path resolution)
- **Read-Only**: `README.md`, `docs/vision.md`

#### 3. Implementation Spec
- **Resolver Architecture**: Introduce a dictionary cache `self.cache` in `WorkspaceResolver`. For each file path checked (`yaml`, `json`, `dir/yaml`, `dir/json`, `evals/yaml`, `evals/json`), before reading the file, check if it exists in the cache and if the file's modification time (`os.path.getmtime(path)`) matches the cached `mtime`. If it matches, return the cached `data`. Otherwise, read the file, store `mtime` and `data` in the cache, and return the `data`.
- **Manifest Format**: None
- **Pseudo-Code**:
  ```python
  class WorkspaceResolver:
      def __init__(self):
          self.cache = {}
      def resolve(self, prompt_id):
          paths_to_try = [f"promptops/prompts/{prompt_id}.yaml", ...]
          for path in paths_to_try:
              if os.path.exists(path):
                  mtime = os.path.getmtime(path)
                  if path in self.cache and self.cache[path]['mtime'] == mtime:
                      data = self.cache[path]['data']
                  else:
                      data = load_prompt_package(path)
                      self.cache[path] = {'mtime': mtime, 'data': data}
                  # Handle quick eval formatting...
                  return data
          return None
  ```
- **Harness Contract Interface**: None
- **Dependencies**: None

#### 4. Test Plan
- **Verification**: Run an eval using the CLI or a test script that resolves the same workspace prompt multiple times. Check if `load_prompt_package` is only called once.
- **Success Criteria**: Repeated `resolve()` calls for the same `prompt_id` from the workspace resolve faster and don't trigger repeated disk reads.
- **Edge Cases**: Modifying the file should trigger a cache invalidation and a new disk read.
