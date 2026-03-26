#### 1. Context & Goal
- **Objective**: Design the resolution logic to fetch prompt packages from OCI registries and language package managers (NPM, PyPI).
- **Trigger**: The docs/vision.md and README.md promises support for OCI artifacts and registry wrappers, but `promptops/resolver/packaged.py` currently raises a `RuntimeError("Protocol not yet implemented for real fetch: {ref}")` for `oci://`, `npm:`, and `pypi:` protocols.
- **Impact**: Unlocks governed distribution capabilities, allowing consumers to securely resolve prompts distributed via standard OCI registries and enterprise package managers.

#### 2. File Inventory
- **Create**: None
- **Modify**: `promptops/resolver/packaged.py`
- **Read-Only**: `promptops/schemas/provider-artifact.schema.json`, `docs/vision.md and README.md`

#### 3. Implementation Spec
- **Resolver Architecture**: Extend the `PackagedResolver._fetch_remote_asset` method to handle `oci://`, `npm:`, and `pypi:` refs. It will route to protocol-specific HTTP API fetchers that download the tarball or manifest, extract the JSON payload, and write it to the local cache fallback directory.
- **Manifest Format**: Support pins formatted as `oci://registry/repo:tag`, `npm:package@version`, and `pypi:package==version`.
- **Pseudo-Code**:
  - If ref starts with `oci://`: Parse registry host and image. Use HTTP GET to fetch OCI manifest, then fetch the blob layer containing the artifact.
  - If ref starts with `npm:`: Query NPM registry for the tarball URL, download, extract `package.json` and artifact payload.
  - If ref starts with `pypi:`: Query PyPI JSON API, locate wheel, extract payload.
- **Harness Contract Interface**: N/A
- **Dependencies**: Depends on existing `provider-artifact.schema.json` from CONTRACTS.

#### 4. Test Plan
- **Verification**: Execute `resolve('my-prompt', 'npm:mock-package@1.0.0')` using a mocked HTTP response and confirm it successfully renders the extracted artifact.
- **Success Criteria**: The `PackagedResolver` returns a valid parsed dictionary for non-HTTPS protocols without raising a RuntimeError.
- **Edge Cases**: Missing package on remote registry, registry downtime (should fallback to cache), malformed tarball, invalid extracted JSON.
