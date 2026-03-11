#### 1. Context & Goal
- **Objective**: Define the final "Packaged Artifact" resolution step for the prompt resolver chain.
- **Trigger**: The Git-first consumption model in `README.md` requires four resolution phases: local override, workspace path, git ref, and packaged artifact. Currently, the Python resolver implements the first three but falls back to `NotImplementedError` instead of resolving packaged artifacts (like GitHub Release assets, OCI digests, or ecosystem wrappers).
- **Impact**: Unlocks governed release consumption. It allows downstream applications to consume stable, published prompt packages instead of relying solely on git SHAs or local paths, completing the end-to-end delivery flow.

#### 2. File Inventory
- **Create**: `.sys/plans/2026-03-11-RUNTIME-PackagedArtifactResolution.md` (This spec file)
- **Modify**: `promptops/resolver/chain.py` (To replace the `NotImplementedError` with the new resolver step)
- **Modify**: A new implementation file in `promptops/resolver/` for the packaged artifact resolver logic.
- **Read-Only**: `README.md` (Governed release packaging options section), `promptops/schemas/consumption-manifest.schema.json`

#### 3. Implementation Spec
- **Resolver Architecture**: Add a new resolver to the end of `ResolverChain`. If a manifest rule contains a packaged artifact reference, this resolver will fetch the bundled package, verify its content digest, and extract the prompt spec.
- **Manifest Format**: The manifest format may need to support an `artifact` or `package` reference if `pin` is strictly meant for git refs. However, since the current schema primarily uses `pin`, the resolver could inspect the `pin` value to determine if it's a URL or digest instead of a git commit.
- **Pseudo-Code**:
  ```python
  class PackagedResolver:
      def resolve(self, prompt_id, ref):
          if is_url_or_digest(ref):
              package = download_and_extract(ref)
              verify_digest(package)
              return extract_prompt(package, prompt_id)
          return None
  ```
  In `ResolverChain.resolve`:
  ```python
  # After GitRefResolver...
  artifact_result = PackagedResolver().resolve(prompt_id, rules['pin'])
  if artifact_result is not None:
      return artifact_result

  raise RuntimeError(f"Failed to resolve '{prompt_id}' via any mechanism.")
  ```
- **Harness Contract Interface**: N/A
- **Dependencies**: Depends on the CONTRACTS domain defining how packaged bundles are structured.

#### 4. Test Plan
- **Verification**:
  ```bash
  mkdir -p test-fixtures
  echo '{"prompts": {"my-prompt": {"id": "my-prompt", "pin": "sha256:12345"}}, "version": "1.0"}' > test-fixtures/mock-artifact-manifest.json
  python -c "from promptops.runtime.resolve import resolve; resolve('my-prompt', 'test-fixtures/mock-artifact-manifest.json')"
  ```
- **Success Criteria**:
  ```bash
  [ $? -eq 0 ]
  ```
- **Edge Cases**:
  ```bash
  echo '{"prompts": {"my-prompt": {"id": "my-prompt", "pin": "sha256:invalid"}}, "version": "1.0"}' > test-fixtures/mock-invalid-artifact.json
  python -c "from promptops.runtime.resolve import resolve; resolve('my-prompt', 'test-fixtures/mock-invalid-artifact.json')"
  [ $? -ne 0 ]
  ```
