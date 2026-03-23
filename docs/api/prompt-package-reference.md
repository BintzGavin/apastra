# Prompt Package Manifest Reference

Immutable bundle of prompt specs with a manifest and content digest.

## Properties

### `id` (string, Required)
Stable identifier for the package.

### `digest` (string, Required)
Content digest of the package, computed over canonicalized JSON using SHA-256.

### `specs` (array[string], Required)
Array of included prompt spec IDs/digests.

### `version` (string, Optional)
Optional semantic version for the package.

### `metadata` (object, Optional)
Optional metadata (e.g., provenance, author).

