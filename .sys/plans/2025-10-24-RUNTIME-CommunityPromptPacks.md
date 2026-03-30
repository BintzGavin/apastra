#### 1. Context & Goal
- **Objective**: Design the implementation spec for Community Prompt Packs to bootstrap a registry using Git dependencies.
- **Trigger**: docs/vision.md outlines Expansion 5 Community prompt packs to curate starter packs as GitHub repos (e.g. Summarization, Extraction, Classification, Code review).
- **Impact**: This expands the resolver chains utility by natively supporting starter pack initialization and bootstrapping the public prompt library registry via Git. Downstream app developers can install these packs.

#### 2. File Inventory
- **Create**: None
- **Modify**: promptops/runtime/cli.py, promptops/resolver/chain.py
- **Read-Only**: docs/vision.md, promptops/schemas/consumption-manifest.schema.json

#### 3. Implementation Spec
- **Resolver Architecture**: The architecture introduces an initialization mechanism for the registry. The resolver chain remains standard. However, the CLI should provide an apastra init or apastra install pack_name command that translates a curated registry name to the official GitHub repo URL and pins the Git ref in the consumption.yaml manifest.
- **Manifest Format**: The manifest format will use the existing pin property for Git-based dependencies: pin: github.com/apastra-registry/summarization-pack@v1.0.0. This leverages GitRefResolver.
- **Pseudo-Code**:
  - Define a curated dictionary of starter packs mapping names to Git URLs.
  - CLI install command accepts a pack name.
  - Fetch the latest tag from the repo.
  - Emit or update the consumption.yaml with the new prompt package mapping, utilizing the Git ref pin format.
- **Harness Contract Interface**: N/A
- **Dependencies**: No new CONTRACTS schemas needed as it reuses consumption.yaml.

#### 4. Test Plan
- **Verification**: Run PYTHONPATH=. python promptops/runtime/cli.py install summarization and confirm consumption.yaml is updated with the correct git ref pin.
- **Success Criteria**: The CLI correctly maps the curated name to the Git repository, retrieves the reference, and updates the manifest.
- **Edge Cases**: Unrecognized pack name, existing manifest entries conflicting, network failure during tag resolution.
