#### 1. Context & Goal
- **Objective**: Spec the reference CLI to resolve prompts using the existing resolver chain and emit consumption manifest entries.
- **Trigger**: The README.md `Phase 1: Protocol and reference implementation` section promises a reference CLI that resolves prompts using local overrides and git refs (commit/tag) and emits a consumption manifest entry.
- **Impact**: Enables end-users and autonomous agents to easily resolve prompts via terminal or shell scripts without using Python APIs directly, lowering the friction to adopt Git-first consumption.

#### 2. File Inventory
- **Create**: A new python script in `promptops/runtime/` to serve as the CLI entrypoint.
- **Modify**: N/A
- **Read-Only**: `README.md` (Phase 1 section)

#### 3. Implementation Spec
- **Resolver Architecture**: The CLI acts as a shell wrapper for the existing `promptops/runtime/resolve.py` logic. It uses the `argparse` module to accept a `prompt_id` and an optional `--ref` context. It calls `resolve(prompt_id, ref_context)` and outputs the rendered prompt template.
- **Manifest Format**: If an optional flag like `--emit-manifest` is provided, the CLI should print a valid YAML object formatted according to `promptops/schemas/consumption-manifest.schema.json`. The output should include a `version: '1.0'` key and a `prompts` object mapping the prompt ID to either an `override` (if the ref looks like a local file path) or a `pin`.
- **Pseudo-Code**:
  ```python
  import argparse
  import yaml
  from promptops.runtime.resolve import resolve

  def main():
      parser = argparse.ArgumentParser()
      parser.add_argument("prompt_id")
      parser.add_argument("--ref", default=None)
      parser.add_argument("--emit-manifest", action="store_true")
      args = parser.parse_args()

      rendered, metadata = resolve(args.prompt_id, args.ref)
      print("--- Resolved Template ---")
      print(rendered)

      if args.emit_manifest:
          entry_type = "override" if args.ref and ('/' in args.ref or '\\' in args.ref) else "pin"
          ref_val = args.ref if args.ref else "latest"
          snippet = {"version": "1.0", "prompts": {args.prompt_id: {"id": args.prompt_id, entry_type: ref_val}}}
          print("--- Manifest Entry ---")
          print(yaml.dump(snippet))
  ```
- **Harness Contract Interface**: N/A
- **Dependencies**: Depends on the existing `promptops/runtime/resolve.py` functionality and CONTRACTS `consumption-manifest.schema.json`.

#### 4. Test Plan
- **Verification**: Run the future CLI script via `run_in_bash_session` targeting a test prompt with `--emit-manifest` enabled.
- **Success Criteria**: The CLI prints the correct rendered template, and the YAML manifest output can be saved to a file and successfully validated against `promptops/schemas/consumption-manifest.schema.json`.
- **Edge Cases**: Missing prompt ID, invalid ref (e.g., invalid git SHA), or ref pointing to a non-existent local file.