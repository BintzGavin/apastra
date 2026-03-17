#### 1. Context & Goal
- **Objective**: Implement missing metadata fields (`dataset digest`, `harness version`) in the `resolve()` function's metadata output as defined in `docs/vision.md`.
- **Trigger**: `docs/vision.md` under "Minimal Runtime" defines the `resolve()` function's metadata as needing to include `prompt digest, dataset digest, harness version, model IDs`. The current implementation in `promptops/runtime/resolve.py` only includes `prompt_digest` and `model`.
- **Impact**: Ensures the minimal runtime satisfies the full "Minimal Runtime" specification from the vision document, allowing consumers (like harnesses) to retrieve and log the complete required environment metadata.

#### 2. File Inventory
- **Create**: None
- **Modify**: `promptops/runtime/resolve.py`
- **Read-Only**: `docs/vision.md`, `.jules/prompts/planning-runtime.md`

#### 3. Implementation Spec
- **Resolver Architecture**: The `resolve()` function should accept `dataset_digest` and `harness_version` as optional keyword arguments.
- **Manifest Format**: N/A
- **Pseudo-Code**:
  - Update `def resolve(prompt_id, ref_context=None, variables=None, dataset_digest=None, harness_version=None):` signature in `promptops/runtime/resolve.py`.
  - In the metadata dictionary construction, conditionally add `dataset_digest` and `harness_version` if they are provided.
  ```python
  metadata = {
      "prompt_digest": compute_digest_from_dict(prompt_spec),
  }
  if model_id:
      metadata["model"] = model_id
  if dataset_digest:
      metadata["dataset_digest"] = dataset_digest
  if harness_version:
      metadata["harness_version"] = harness_version
  ```
- **Harness Contract Interface**: N/A
- **Dependencies**: N/A

#### 4. Test Plan
- **Verification**: `python3 -c "from promptops.runtime.resolve import resolve; print(resolve('summarize', dataset_digest='abc', harness_version='v1'))"`
- **Success Criteria**: The function returns a tuple containing the rendered prompt and a metadata dictionary containing `dataset_digest` and `harness_version`.
- **Edge Cases**: Function called without the new optional arguments (should retain backwards compatibility).
