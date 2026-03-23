# Provider Artifact Manifest Reference

A distribution wrapper around a prompt package (git ref, release asset, OCI artifact, npm/PyPI wrapper).

## Properties

### `id` (string, Required)
Stable identifier for the provider artifact.

### `type` (string, Required)
The distribution type of the wrapper.
**Enum values:** git_ref, release_asset, oci_artifact, npm_wrapper, pypi_wrapper

### `reference` (string, Required)
The URI, ref, or tag of the wrapper.

### `package_digest` (string, Required)
Content digest of the underlying prompt package.

### `metadata` (object, Optional)
Arbitrary key-value pairs for registry-specific data, provenance, or signatures.

