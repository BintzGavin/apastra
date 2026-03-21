# Context: RUNTIME Domain

## Section A: Architecture
The promptops runtime resolves prompt templates deterministically. The resolution chain executes in this explicit order:
1. **Local Override**: Resolves to a local file path if specified in the manifest. Includes memory caching based on the file's modification time.
2. **Workspace Path**: Looks for the prompt file directly in `promptops/prompts/` within the repository. Includes memory caching based on the file's modification time.
3. **Git Ref**: Fetches the prompt specification directly from git using a specified tag or commit SHA. Includes memory caching based on `(prompt_id, pin)`. If the target git host prevents archive downloads, it falls back to a shallow clone for tags/branches, or a full clone followed by checkout for specific commit SHAs.
4. **Packaged Artifact**: Falls back to packaged assets when resolving remote references (e.g., via sha256).

## Section B: File Tree
```
promptops/
├── runtime/
│   ├── __init__.py
│   ├── digest.py
│   ├── render.py
│   └── resolve.py
├── resolver/
│   ├── __init__.py
│   ├── chain.py
│   ├── git_ref.py
│   ├── local.py
│   ├── packaged.py
│   └── workspace.py
└── manifests/
    ├── __init__.py
    └── consumption.py
```

## Section C: Public Interface
```python
def resolve(prompt_id: str, ref_context=None, variables: dict=None, dataset_digest: str=None, harness_version: str=None, model_ids: list=None) -> tuple[str, dict]:
    # Returns rendered_prompt_string, metadata_dict (including provenance if applicable)
```

Exceptions:
- `RuntimeError` if resolution fails, or schema validation fails.

## Section D: Manifest Format
```yaml
version: "1.0"
prompts:
  "my-stable-id":
    id: "actual-prompt-id"
    pin: "v1.0.0"          # Optional Git ref, package pin, or registry URI (npm:, pypi:, oci://)
    override: "./local"    # Optional local override path
    model: "gpt-4"         # Optional default model to use
defaults:
  model: "gpt-3.5-turbo"
```

## Section E: Integration Points
- **EVALUATION**: Harnesses call `resolve(prompt_id, ...)`, which returns the prompt template and a metadata block to attach to the runner execution payload.
- **GOVERNANCE**: No direct API dependencies; relies on deterministic artifacts emitted by EVALUATION.
