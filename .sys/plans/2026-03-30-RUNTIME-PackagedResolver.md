#### 1. Context & Goal
- **Objective**: Implement the `PackagedResolver` to parse and resolve `prompt-package` and `provider-artifact` bundles correctly, rather than relying on a mock implementation.
- **Trigger**: The current `promptops/resolver/packaged.py` provides a stub/mock resolution for OCI and sha256 refs, which leaves a gap in the `Packaged artifact` vision requirement for governed releases.
- **Impact**: This unlocks true consumption of packaged artifacts (e.g. OCI digests, release assets) defined in a consumption manifest, allowing EVALUATION and GOVERNANCE domains to interact with published prompt packages.

#### 2. File Inventory
- **Create**: None
- **Modify**: `promptops/resolver/packaged.py`
- **Read-Only**: `docs/vision.md`, `README.md`, `promptops/schemas/prompt-package.schema.json`, `promptops/schemas/provider-artifact.schema.json`

#### 3. Implementation Spec
- **Resolver Architecture**: Update `PackagedResolver` to distinguish between direct prompt-package digests and provider-artifact metadata wrappers. The resolver chain remains intact, delegating to `PackagedResolver` when `pin` starts with `sha256:` or `oci://`.
- **Manifest Format**: Uses the existing consumption manifest format where `pin: sha256:...` resolves to a packaged artifact.
- **Pseudo-Code**:
  - In `PackagedResolver.resolve(prompt_id, ref)`:
    - If `ref.startswith('sha256:')`: Treat as a direct content digest for a prompt package (or provider artifact). Parse the referenced package, validate against `prompt-package.schema.json`, extract the spec for `prompt_id`.
    - If `ref.startswith('oci://')`: Resolve the OCI registry reference, fetch the manifest, validate against `provider-artifact.schema.json`, then retrieve the underlying `package_digest` and validate the prompt package.
- **Harness Contract Interface**: N/A
- **Dependencies**: Depends on the existing CONTRACTS schemas `prompt-package.schema.json` and `provider-artifact.schema.json`.

#### 4. Test Plan
- **Verification**: `python3 -c "from promptops.resolver.packaged import PackagedResolver; print(PackagedResolver().resolve('test-prompt', 'sha256:mock_digest_test'))"`
- **Success Criteria**: The resolver correctly routes the packaged reference format and attempts a validation/extraction workflow, raising expected errors for unresolved remote assets instead of returning a stub template.
- **Edge Cases**: Malformed digests, missing prompt spec IDs in the prompt package array, invalid OCI URLs.
