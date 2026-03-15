## Section A: Architecture
1. **Local Override**: Checked first via manifest (`override: path/to/file.yaml`).
2. **Workspace**: Fallback to checking `./promptops/prompts/<prompt_id>/prompt-spec.yaml` or `.json` or just `<prompt_id>.yaml`/`<prompt_id>.json`.
3. **Git Ref / Packaged**: Fallback to fetching via `git checkout` (SHA or semver tag) or pulling OCI artifacts if a `pin` is present in the manifest.
*Note: The ID used in the resolver chain is the mapped `id` from the manifest (defaulting to the requested `prompt_id`), allowing aliases.*

## Section B: File Tree
```
promptops/
├── runtime/
│   ├── resolve.py
│   ├── render.py
│   ├── digest.py
│   └── runner.py
├── resolver/
│   ├── chain.py
│   ├── local.py
│   ├── workspace.py
│   ├── git_ref.py
│   └── packaged.py
└── manifests/
    └── consumption.yaml
```

## Section C: Public Interface
```python
def load_manifest(ref_context=None) -> ManifestWrapper:
    pass

def resolve(prompt_id: str, ref_context: str = None, variables: dict = None) -> tuple[str, dict]:
    # Returns (rendered_prompt_string, metadata_dict)
    # metadata_dict contains 'prompt_digest' (str) and optionally 'model' (str) if specified in manifest.
    pass

def compute_digest(file_path: str) -> str:
    pass

def compute_digest_from_dict(data: dict) -> str:
    pass
```

## Section D: Manifest Format
```yaml
version: "1.0"
defaults:
  model: gpt-3.5-turbo
prompts:
  summarize:             # App alias
    id: summarize-v1     # Stable ID mapped
    model: gpt-4         # Specific model override
    pin: v1.0.0          # Git ref or tag
  analyze:
    override: ./local-prompts/analyze.json
```
- Local names can map to actual backend IDs using `id`.
- Support specifying `model` explicitly.

## Section E: Integration Points
- **EVALUATION**: Harnesses use `resolve()` to get the template, compute digests for verification, and retrieve model configuration from metadata.
- **GOVERNANCE**: Policy gates read manifest fields to enforce model usage and digest checks.
