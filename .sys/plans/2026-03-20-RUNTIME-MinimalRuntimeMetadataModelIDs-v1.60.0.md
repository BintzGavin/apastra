#### 1. Context & Goal
- **Objective**: Implement the `model IDs` array in the `resolve()` function's metadata output.
- **Trigger**: The docs/vision.md file specifies that the minimal runtime `resolve()` function must output metadata containing `prompt digest, dataset digest, harness version, model IDs`. Currently, `model_id` is only supported as a single string instead of the plural `model_ids` array, missing this vision gap.
- **Impact**: Ensures that the `resolve()` function fully implements the promised minimal runtime interface, unlocking downstream capability for EVALUATION harnesses to consume and log the complete environment metadata matrix correctly.

#### 2. File Inventory
- **Create**: None
- **Modify**: `promptops/runtime/resolve.py`
- **Read-Only**: `docs/vision.md`, `README.md`, `promptops/schemas/run-manifest.schema.json`

#### 3. Implementation Spec
- **Resolver Architecture**: The `resolve()` function's signature and implementation will be updated to accept `model_ids` (as a list of strings) and place it in the metadata dictionary if provided, replacing the current single `model` logic.
- **Manifest Format**: Update rule parsing to map a singular `model` key to a single-element list in `model_ids` if no explicit array is passed.
- **Pseudo-Code**:
  ```python
  def resolve(prompt_id, ref_context=None, variables=None, dataset_digest=None, harness_version=None, model_ids=None):
      manifest = load_manifest(ref_context)
      ...
      rules = manifest.get_rules(prompt_id) if hasattr(manifest, 'get_rules') else {}
      defaults = manifest.data.get('defaults', {}) if hasattr(manifest, 'data') and isinstance(manifest.data, dict) else {}

      # Determine model_ids
      if model_ids is None:
          model = rules.get('model', defaults.get('model'))
          if model:
              model_ids = [model]

      metadata = {
          "prompt_digest": compute_digest_from_dict(prompt_spec),
      }
      if model_ids:
          metadata["model_ids"] = model_ids
      if dataset_digest:
          metadata["dataset_digest"] = dataset_digest
      if harness_version:
          metadata["harness_version"] = harness_version
  ```
- **Harness Contract Interface**: Input: `run_request.json` with revision ref. Output: `run_artifact` directory compliant with schema.
- **Dependencies**: Depends on the existing `promptops/schemas/consumption-manifest.schema.json` and `promptops/schemas/prompt-spec.schema.json`.

#### 4. Test Plan
- **Verification**: `python3 -c "from promptops.runtime.resolve import resolve; print(resolve('summarize', dataset_digest='abc', harness_version='v1', model_ids=['gpt-4']))"`
- **Success Criteria**: The metadata dictionary returned correctly contains `"model_ids": ["gpt-4"]` instead of `"model": "gpt-4"`.
- **Edge Cases**: Function called without `model_ids` provided should extract it from manifest rules/defaults and output a list if available. Function called with no model info available should just omit `model_ids` from metadata.
