#### 1. Context & Goal
- **Objective**: Implement caching of local overrides to support offline fallback and improve performance in the RUNTIME domain.
- **Trigger**: The docs/vision.md state that "Local iteration must not require publishing artifacts" and "consumption must be simpler than authoring". The `LocalResolver` currently reads the file on every resolution, which could be slow for large overrides or repetitive evaluations.
- **Impact**: Improves performance of the resolver chain for local overrides, unlocking faster local iteration and evaluation runs, aligning with the "Git-first consumption" and "local override" vision.

#### 2. File Inventory
- **Create**: None
- **Modify**: `promptops/resolver/local.py`
- **Read-Only**: `docs/vision.md`

#### 3. Implementation Spec
- **Resolver Architecture**: The `LocalResolver` will cache the loaded prompt package data in an instance-level dictionary based on the file modification time and path. Before loading the file, it will check if it's already in the cache and if the file hasn't been modified since it was cached. If so, it returns the cached data. Otherwise, it loads the file, updates the cache, and returns the data.
- **Manifest Format**: None
- **Pseudo-Code**:
  ```python
  class LocalResolver:
      def __init__(self):
          self.cache = {}

      def resolve(self, prompt_id, override_path):
          if not os.path.exists(override_path):
              raise FileNotFoundError(f"Local override path not found: {override_path}")

          mtime = os.path.getmtime(override_path)

          if override_path in self.cache and self.cache[override_path]['mtime'] == mtime:
              data = self.cache[override_path]['data']
          else:
              data = load_prompt_package(override_path)
              self.cache[override_path] = {'mtime': mtime, 'data': data}

          # Quick eval resolution...
  ```
- **Harness Contract Interface**: None
- **Dependencies**: None

#### 4. Test Plan
- **Verification**: Run a simple python script that resolves the same local override twice and verify that `load_prompt_package` is only called once.
- **Success Criteria**: The local resolver successfully resolves a local override path, and caches the result for subsequent calls if the file hasn't changed.
- **Edge Cases**: Modifying the file should invalidate the cache and reload the data. File not found should raise `FileNotFoundError`.
