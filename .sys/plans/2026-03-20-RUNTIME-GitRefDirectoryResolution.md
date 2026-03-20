#### 1. Context & Goal
- **Objective**: Implement Git Ref Resolution for Directory-Based Prompts.
- **Trigger**: The vision document allows prompt packages to be structured as a directory (`promptops/prompts/<prompt_id>/prompt.yaml`). The current `GitRefResolver` implementation might not consistently resolve this structure across all Git commands and remote fetches.
- **Impact**: Enables `GitRefResolver` to correctly handle both flat file and directory-based prompt packages, aligning with `WorkspaceResolver` capabilities and fully supporting Git-first consumption.

#### 2. File Inventory
- **Create**: `.sys/plans/2026-03-20-RUNTIME-GitRefDirectoryResolution.md` (Spec for GitRef directory resolution)
- **Modify**: None
- **Read-Only**: `docs/vision.md`, `README.md`, `promptops/schemas/prompt-spec.schema.json`

#### 3. Implementation Spec
- **Resolver Architecture**: The `GitRefResolver` must execute `git show` sequentially: checking flat yaml/json files first, followed by directory-based `prompt.yaml` and `prompt.json`. This maintains parity with the `WorkspaceResolver`.
- **Manifest Format**: Unchanged.
- **Pseudo-Code**:
  - Inside `GitRefResolver.resolve(prompt_id, pin)`:
    - After matching the semver/pin logic:
    - Try `git show <pin>:promptops/prompts/<prompt_id>.yaml` -> return if success
    - Try `git show <pin>:promptops/prompts/<prompt_id>.json` -> return if success
    - Try `git show <pin>:promptops/prompts/<prompt_id>/prompt.yaml` -> return if success
    - Try `git show <pin>:promptops/prompts/<prompt_id>/prompt.json` -> return if success
    - Finally try the quick evals path (`promptops/evals/`).
- **Harness Contract Interface**: Unchanged. Interface is still `resolve(prompt_id, ref_context=None, ...)`.
- **Dependencies**: Depends on the existing `prompt-spec.schema.json` to ensure resolved specs conform to the correct format.

#### 4. Test Plan
- **Verification**: Run `resolve('my-dir-prompt', ref_context={'prompts': {'my-dir-prompt': {'pin': 'v1.0.0'}}})` where `v1.0.0` points to a commit with the file located at `promptops/prompts/my-dir-prompt/prompt.yaml`.
- **Success Criteria**: The resolver correctly fetches, parses, and returns the rendered prompt string and metadata from the directory structure.
- **Edge Cases**: Missing files, invalid yaml/json within the directory package, Git connection errors.
