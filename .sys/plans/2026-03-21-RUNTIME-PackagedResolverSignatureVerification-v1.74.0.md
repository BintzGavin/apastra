#### 1. Context & Goal
- **Objective**: Implement robust cryptographic signature verification in the PackagedResolver for provider artifacts.
- **Trigger**: The vision document explicitly lists supply-chain tampering prevention as a key feature (e.g. "Immutable releases; attestations; digest pinning") and calls for verifying signatures/attestations optionally. The current `verify_signature` method in `promptops/resolver/packaged.py` contains stub logic that only checks if a metadata field explicitly equals 'invalid'.
- **Impact**: Strengthens the Black Hole architecture's supply-chain posture by actually validating provenance and signatures on downloaded artifacts before returning their prompt specs, protecting consumers from malicious remote packages.

#### 2. File Inventory
- **Create**: None
- **Modify**: `promptops/resolver/packaged.py` (Enhance `verify_signature` to perform actual cryptographic checks using standard libraries or placeholder standard patterns instead of purely checking for the string 'invalid').
- **Read-Only**: `docs/vision.md` (Provenance and signing section), `README.md`.

#### 3. Implementation Spec
- **Resolver Architecture**:
  - The `PackagedResolver.verify_signature(asset)` method will be expanded.
  - It will check the artifact type (e.g., `oci_artifact`, `npm`, `pypi`) and look for corresponding signature formats (e.g., sigstore bundles, standard PGP signatures, or SLSA provenance attestations).
  - The architecture will define how to configure trusted public keys or trust roots (e.g., via environment variables or a configuration file).
  - It will perform actual cryptographic verification (using a library like `cryptography` or calling out to tools like `cosign` if available, or providing a robust extensible structure if external tools are not mandated in the minimal runtime).
- **Manifest Format**: No changes.
- **Pseudo-Code**:
  ```python
  def verify_signature(self, asset):
      # Extract signature block from asset metadata
      signature = asset.get('metadata', {}).get('signature')
      if not signature:
          # If strict mode is on, raise Error; else warn/pass
          return True

      if signature == 'invalid':
          raise RuntimeError("Signature verification failed")

      artifact_type = asset.get('type')
      public_key = self.get_trusted_public_key(artifact_type)

      # Perform actual cryptographic verification depending on type
      # (e.g., verifying a JWT or using a library to verify a signed payload)
      # if not valid_crypto_check(asset['package_digest'], signature, public_key):
      #     raise RuntimeError("Cryptographic signature verification failed")

      return True
  ```
- **Harness Contract Interface**: No changes required.
- **Dependencies**: No new CONTRACTS schemas required.

#### 4. Test Plan
- **Verification**: Write a test script `test_verify_signature.py` that mocks `urllib.request` to return a packaged artifact with a valid signature and one with an invalid signature, and asserts `PackagedResolver().resolve` raises an error on the invalid one.
- **Success Criteria**: The resolver correctly rejects an artifact with an invalid cryptographic signature and accepts a valid one.
- **Edge Cases**: Missing signature, unsupported signature format, expired certificates, mismatched public keys.
