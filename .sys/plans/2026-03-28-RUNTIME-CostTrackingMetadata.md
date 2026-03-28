#### 1. Context & Goal
- **Objective**: Include token cost estimates in resolved prompt metadata.
- **Trigger**: The docs/vision.md document proposes "Cost tracking in resolver metadata" as an expansion feature.
- **Impact**: Enables consumers and evaluators to track cost metrics.

#### 2. File Inventory
- **Create**: None
- **Modify**: `promptops/runtime/resolve.py`
- **Read-Only**: `promptops/schemas/run-manifest.schema.json`

#### 3. Implementation Spec
- **Resolver Architecture**: Add `estimated_cost` to the metadata dictionary in `resolve()`.
- **Manifest Format**: Uses `max_tokens` from rules, manifest defaults, or project config to estimate costs.
- **Pseudo-Code**:
  ```python
  def resolve(prompt_id, ...):
      ...
      max_tokens = rules.get('max_tokens', defaults.get('max_tokens', project_defaults.get('max_tokens', 0)))
      if max_tokens and model_ids:
          estimated_cost = max_tokens * 0.00001
          metadata["estimated_cost"] = estimated_cost
      ...
  ```
- **Harness Contract Interface**: Downstream harnesses receive `estimated_cost`.
- **Dependencies**: Relies on EVALUATION/CONTRACTS cost fields.

#### 4. Test Plan
- **Verification**: Run `resolve('test')` with a manifest defining `max_tokens`.
- **Success Criteria**: The metadata includes `estimated_cost`.
- **Edge Cases**: Missing `max_tokens`.
