#### 1. Context & Goal
- **Objective**: Implement quick eval format resolution in the WorkspaceResolver to treat single-file eval configs as prompt specs.
- **Trigger**: `docs/vision.md` mentions "Quick eval mode" where a single file in `promptops/evals/` contains `prompt`, `cases`, and `assertions`. "The agent reads a quick eval file and internally treats it as a prompt spec...".
- **Impact**: Enables rapid iteration smoke tests by parsing `promptops/evals/my-eval.yaml` and returning a valid prompt spec object (`id`, `template`, `variables` inferred from template or empty).

#### 2. File Inventory
- **Create**: None
- **Modify**: `promptops/resolver/workspace.py`
- **Read-Only**: `promptops/schemas/quick-eval.schema.json`, `docs/vision.md`

#### 3. Implementation Spec
- **Resolver Architecture**: Update `WorkspaceResolver.resolve()` to also look for files in `promptops/evals/{prompt_id}.yaml` or `promptops/evals/{prompt_id}.json`. If found, convert the quick eval schema (which has `id`, `prompt`) into a `prompt-spec` compatible dictionary: `{"id": quick_eval["id"], "template": quick_eval["prompt"], "variables": {}}`.
- **Manifest Format**: N/A
- **Pseudo-Code**:
  ```python
  class WorkspaceResolver:
      def resolve(self, prompt_id):
          # existing promptops/prompts/ checks...

          # Quick eval resolution
          quick_eval_yaml = f"promptops/evals/{prompt_id}.yaml"
          if os.path.exists(quick_eval_yaml):
              data = load_prompt_package(quick_eval_yaml)
              if data and "prompt" in data:
                  return {"id": prompt_id, "template": data["prompt"], "variables": {}}

          quick_eval_json = f"promptops/evals/{prompt_id}.json"
          if os.path.exists(quick_eval_json):
              data = load_prompt_package(quick_eval_json)
              if data and "prompt" in data:
                  return {"id": prompt_id, "template": data["prompt"], "variables": {}}

          return None
  ```
- **Harness Contract Interface**: N/A
- **Dependencies**: CONTRACTS `quick-eval.schema.json`

#### 4. Test Plan
- **Verification**: `mkdir -p promptops/evals && echo 'id: my-quick-eval\nprompt: "Quick prompt"' > promptops/evals/my-quick-eval.yaml && python -c "from promptops.resolver.workspace import WorkspaceResolver; print(WorkspaceResolver().resolve('my-quick-eval'))"`
- **Success Criteria**: Returns `{'id': 'my-quick-eval', 'template': 'Quick prompt', 'variables': {}}`.
- **Edge Cases**: Regular prompts still resolve correctly.
