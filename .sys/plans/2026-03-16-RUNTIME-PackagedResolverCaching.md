#### 1. Context & Goal
- **Objective**: Implement local caching, offline fallback, and optional signature verification in the PackagedResolver.
- **Trigger**: `docs/vision.md` specifies that the SDKs should support local caching, offline fallback, and optional signature verification, which are currently missing in `promptops/resolver/packaged.py`.
- **Impact**: Enables low-latency retrieval, offline execution, and verifiable trust for downstream consumers.

#### 2. File Inventory
- **Create**: None
- **Modify**: `promptops/resolver/packaged.py` to add local caching, offline fallback, and signature verification logic.
- **Read-Only**: `docs/vision.md`, `promptops/schemas/provider-artifact.schema.json`, `promptops/schemas/prompt-package.schema.json`

#### 3. Implementation Spec
- **Resolver Architecture**: The `PackagedResolver` will first check a local cache directory for the requested digest or reference. If found, it returns the cached asset (offline fallback). If not found, it fetches the remote asset, validates the schema, optionally verifies attestations/signatures if configured, and writes the valid asset to the local cache before returning it.
- **Manifest Format**: No changes to the consumption manifest format.
- **Pseudo-Code**:
  1. Generate cache file path based on `ref`.
  2. If cache file exists, load asset from cache.
  3. If signature verification is enabled, verify signature.
  4. If valid, extract and return `prompt_id`.
  5. If not cached (or invalid), fetch remote asset via `_fetch_remote_asset()`.
  6. Validate against schema.
  7. Verify signature/attestation if enabled.
  8. Save asset to cache file path.
  9. Extract and return `prompt_id` from asset.
- **Harness Contract Interface**: None.
- **Dependencies**: Depends on existing CONTRACTS schemas `promptops/schemas/provider-artifact.schema.json` and `promptops/schemas/prompt-package.schema.json`.

#### 4. Test Plan
- **Verification**: echo 'No tests to run for Architect Planner'
- **Success Criteria**: The spec provides a clear architecture for adding caching and signature verification to the PackagedResolver.
- **Edge Cases**: Missing cache directory, corrupted cache files, invalid signatures, network failure during remote fetch.
