#### 1. Context & Goal
- **Objective**: Implement npm and PyPI wrapper resolution in the PackagedResolver.
- **Trigger**: The vision document explicitly lists npm/PyPI wrappers as supported packaging options ("Optional packaging for governed releases. When teams want stronger distribution guarantees, use GitHub immutable releases, OCI digests, and SLSA-style provenance attestations. ... npm/PyPI wrapper"), but the current `PackagedResolver` only handles `sha256:`, `https://`, and `oci://` refs.
- **Impact**: Unlocks app-side consumption of prompt packages published to ecosystem registries like npm and PyPI, supporting governed release distribution.

#### 2. File Inventory
- **Create**: None
- **Modify**: `promptops/resolver/packaged.py` (Update `resolve` to handle `npm:` and `pypi:` schema prefixes, fetch the wrapper, parse the provider artifact, and recursively resolve the package digest). Update `promptops/resolver/chain.py` (Update `pin` prefix checking to also allow `npm:` and `pypi:` prefixes to be routed to `PackagedResolver`).
- **Read-Only**: `docs/vision.md` (Governed release packaging options), `promptops/schemas/provider-artifact.schema.json` (Validating the fetched wrapper).

#### 3. Implementation Spec
- **Resolver Architecture**: The `ResolverChain` will route pins starting with `npm:` or `pypi:` to the `PackagedResolver`. The `PackagedResolver` will interpret these prefixes, mock fetch the wrapper asset (as with other remote refs), validate the returned provider artifact against `provider-artifact.schema.json`, extract the `package_digest`, and recursively resolve it.
- **Manifest Format**: Manifest pins will support `npm:<package>@<version>` or `pypi:<package>==<version>` syntaxes. Validation rules remain unchanged as pins are just string references.
- **Pseudo-Code**:
  In `chain.py`:
  if pin.startswith(('sha256:', 'https://', 'oci://', 'npm:', 'pypi:')):
      return PackagedResolver().resolve(target_id, pin)
  In `packaged.py`:
  if ref.startswith(('https://', 'oci://', 'npm:', 'pypi:')):
      asset = self._fetch_remote_asset(ref)
      validate against provider-artifact schema
      return self.resolve(prompt_id, asset.get('package_digest'))
- **Harness Contract Interface**: N/A
- **Dependencies**: Depends on the existing CONTRACTS schema `provider-artifact.schema.json`.

#### 4. Test Plan
- **Verification**: python3 -c 'from promptops.resolver.chain import ResolverChain; print(ResolverChain().resolve("my-prompt", {"prompts": {"my-prompt": {"pin": "npm:my-package@1.0.0"}}}))'
- **Success Criteria**: The resolution returns the correct prompt spec dictionary.
- **Edge Cases**: Invalid npm/PyPI ref format, unreachable registry, invalid provider artifact schema in the wrapper.
