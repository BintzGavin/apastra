#### 1. Context & Goal
- **Objective**: Implement quick eval format resolution in the GitRefResolver to treat single-file eval configs as prompt specs when resolving from a git commit or tag.
- **Trigger**: `docs/vision.md` mentions "Quick eval mode" where a single file in `promptops/evals/` contains `prompt`, `cases`, and `assertions`. "The agent reads a quick eval file and internally treats it as a prompt spec...". This was implemented for the workspace resolver, and parity is required for the git ref resolver.
- **Impact**: Enables rapid iteration smoke tests by parsing `promptops/evals/my-eval.yaml` from a git ref and returning a valid prompt spec object (`id`, `template`, `variables` inferred from template or empty).

#### 2. File Inventory
- **Create**: None
- **Modify**: `promptops/resolver/git_ref.py`
- **Read-Only**: `promptops/schemas/quick-eval.schema.json`, `docs/vision.md`

#### 3. Implementation Spec
- **Resolver Architecture**: Update `GitRefResolver.resolve()` to also look for files via `git show {pin}:promptops/evals/{prompt_id}.yaml` or `.json`. If found, convert the quick eval schema (which has `id`, `prompt`) into a `prompt-spec` compatible dictionary: `{"id": prompt_id, "template": data["prompt"], "variables": {}}`.
- **Manifest Format**: N/A
- **Pseudo-Code**:
  ```python
  class GitRefResolver:
      def resolve(self, prompt_id, pin):
          # existing git tag / pin logic...

          # existing promptops/prompts/ checks...

          # Quick eval resolution
          result_eval_yaml = subprocess.run(
              ["git", "show", f"{pin}:promptops/evals/{prompt_id}.yaml"],
              capture_output=True, text=True, check=False
          )
          if result_eval_yaml.returncode == 0:
              data = yaml.safe_load(result_eval_yaml.stdout)
              if data and "prompt" in data:
                  return {"id": prompt_id, "template": data["prompt"], "variables": {}}

          result_eval_json = subprocess.run(
              ["git", "show", f"{pin}:promptops/evals/{prompt_id}.json"],
              capture_output=True, text=True, check=False
          )
          if result_eval_json.returncode == 0:
              data = json.loads(result_eval_json.stdout)
              if data and "prompt" in data:
                  return {"id": prompt_id, "template": data["prompt"], "variables": {}}

          raise RuntimeError(f"Failed to resolve prompt '{prompt_id}' at git ref '{pin}'")
  ```
- **Harness Contract Interface**: N/A
- **Dependencies**: CONTRACTS `quick-eval.schema.json`

#### 4. Test Plan
- **Verification**: `mkdir -p promptops/evals && echo 'id: my-git-eval\nprompt: "Git quick prompt"' > promptops/evals/my-git-eval.yaml && git add promptops/evals/my-git-eval.yaml && git commit -m "Add quick eval" && python -c "from promptops.resolver.git_ref import GitRefResolver; print(GitRefResolver().resolve('my-git-eval', 'HEAD'))"`
- **Success Criteria**: Returns `{'id': 'my-git-eval', 'template': 'Git quick prompt', 'variables': {}}`.
- **Edge Cases**: Regular prompts still resolve correctly; handles git missing file errors correctly without crashing.
