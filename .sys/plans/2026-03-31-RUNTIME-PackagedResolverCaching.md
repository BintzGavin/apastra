#### 1. Context & Goal
- **Objective**: Implement real remote asset fetching, local caching, offline fallback, and signature verification in the `PackagedResolver`.
- **Trigger**: The current `PackagedResolver` uses a mock implementation for fetching remote assets (`_fetch_remote_asset`) and verifying signatures (`verify_signature`), which fails to satisfy the vision document's requirement for robust packaged artifact resolution and supply-chain integrity.
- **Impact**: Enables genuine consumption of remote packaged artifacts (OCI, npm, PyPI, http) with resilience against network failures (offline fallback) and cryptographic verification of supply-chain attestations.

#### 2. File Inventory
- **Create**: None
- **Modify**: `promptops/resolver/packaged.py`
- **Read-Only**: `docs/vision.md`, `README.md`, `promptops/schemas/provider-artifact.schema.json`

#### 3. Implementation Spec
- **Resolver Architecture**: Replace the mock `_fetch_remote_asset` with actual fetching logic (e.g., using `urllib` or appropriate subprocess commands for OCI/npm). Implement robust cache checking so that if the network fails, it gracefully falls back to the locally cached asset.
- **Manifest Format**: Unchanged.
- **Pseudo-Code**:
  - In `PackagedResolver._fetch_remote_asset(ref)`:
    - Determine protocol (https, oci, npm, pypi).
    - Attempt to fetch the remote asset.
    - If fetch is successful, write to `cache_path`.
    - If fetch fails (network error) and `cache_path` exists, load from `cache_path` (offline fallback).
    - If fetch fails and no cache exists, raise `RuntimeError`.
  - In `PackagedResolver.verify_signature(asset)`:
    - Extract signature metadata from the asset.
    - Implement real cryptographic verification depending on the artifact type.
- **Harness Contract Interface**: N/A
- **Dependencies**: Depends on CONTRACTS schemas for `provider-artifact.schema.json`.

#### 4. Test Plan
- **Verification**: echo 'No tests to run for Architect Planner'
- **Success Criteria**: The resolver successfully fetches a real remote asset, caches it locally, can serve it while offline, and properly authenticates its signature.
- **Edge Cases**: Network offline with no cache, corrupted cache file, invalid or missing signature metadata.