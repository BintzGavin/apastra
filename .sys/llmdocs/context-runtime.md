## Section A: Architecture
1. **Local Override**: Checked first via manifest (`override: path/to/file.yaml`).
2. **Workspace**: Fallback to checking `./promptops/prompts/<prompt_id>/prompt-spec.yaml` or `.json` or just `<prompt_id>.yaml`/`<prompt_id>
 .json`.
3. **Git Ref / Packaged**: Fallback to fetching via `git checkout` (SHA or semver tag) or pulling OCI artifacts, npm packages, or PyPI packages if a `pin` is present in the manifest.
*Note: The ID used in the resolver chain is the mapped `id
`  from the manifest (defaulting to the requested `prompt_id`), allowing aliases.*

## Section B: File Tree
```
promptops/
âââ runtime/
â   âââ resolve.py
â   âââ render.py
â   âââ digest.py
â   âââ runner.py
Ã¢\
xc2 \x94Â\xe2\x94 \x80Ã¢Ââ resolver/
â   âââ chain.py
â   âââ local.py
â   âââ workspace.py
â   âââ git_ref.py
â   âââ packaged.py
âââ manifests/
    âââ consumption.yaml
```

## Section C: P ubl
ic Inter face
```python
def  load_manifest(ref_context=None) -> ManifestWrapper:
     pass

class PackagedResolver:
    def resolve(self, prompt_id: str, ref: str) -> dict:
        pass
    def verify_signature(self, asset: dict) -> bool:
        pass


def res olve(prompt_id: str , ref_context: str = None, variables: dict = None, dataset_digest: str = None, harness_version: str = None) -> tuple[str, dict]:
    # Returns (rendered_prompt_string, metadata_dict)
    # metadata_dict contains 'pr ompt_
digest' (s tr) and optionally ' model', 'dataset_digest', and 'harness_version' if specified.
    pass

def compute_digest(file_path: str) -> str:
    pass

def compute_digest_from_dict(data: dict) -> str:
    pass
```

## Section D: Manifest F ormat

```yaml
ver sion: "1.0"
defaults:
  model: gpt-3.5-turbo
prompts:
  summarize:             # App alias
    id: summarize-v1     # Stable ID mapped
    model: gpt-4         # Specific model override
    pin: v1.0.0          # Git ref or tag
  a nalyze:

    overrid e: ./local-prompts/analyze.json
```
- Local names can map to actual backend IDs using `id`.
- Support specifying `model` explicitly.

## Section E: Integration Points
- **EVALUATION**: Harnesses use `resolve()` to get the templat e, compu
te digests fo r verification, and retrieve model configuration from metadata.
- **GOVERNANCE**: Policy gates read manifest fields to enforce model usage and digest checks