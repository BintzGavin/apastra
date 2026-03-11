#### 1. Context & Goal
- **Objective**: Create the JSON Schema and a bash validator script for Provider Artifacts.
- **Trigger**: The `README.md` defines a provider artifact as a "A distribution wrapper around a prompt package (git ref, release asset, OCI artifact, npm/PyPI wrapper)." This is the last remaining core noun from the README's core nouns table that lacks a machine-readable schema.
- **Impact**: Enables standardizing the structure for distribution wrappers, unlocking robust artifact retrieval, resolution, and governed releases across the system.

#### 2. File Inventory
- **Create**:
  - A JSON schema file for provider artifacts defining the structure of a provider artifact.
  - A bash validator script for provider artifacts to validate provider artifacts against the schema using `ajv-cli`.
- **Modify**: None.
- **Read-Only**: `README.md`.

#### 3. Implementation Spec
- **Schema Architecture**:
  - Format: JSON Schema (draft 2020-12).
  - Required fields:
    - `id` (string): Stable identifier.
    - `type` (string, enum: `git_ref`, `release_asset`, `oci_artifact`, `npm_wrapper`, `pypi_wrapper`): The distribution type.
    - `reference` (string): The URI, ref, or tag of the wrapper.
    - `package_digest` (string): Content digest of the underlying prompt package, matching pattern `^sha256:[a-f0-9]{64}$`.
  - Optional fields:
    - `metadata` (object): Arbitrary key-value pairs for registry-specific data, provenance, or signatures.
- **Content Digest Convention**:
  - Does not compute its own content digest inherently, but relies heavily on storing the `package_digest` referencing the prompt package it wraps.
- **Pseudo-Code**:
  - The validation script will execute: `npx --yes ajv-cli validate -s <path_to_conceptual_schema_file> -d "$1" --spec=draft2020 --strict=false -c ajv-formats`
- **Public Contract Changes**:
  - Exports a new schema for provider artifacts to be used by publishers and consumption resolvers.
- **Dependencies**: None.

#### 4. Test Plan
- **Verification**:
  - `mkdir -p test-fixtures`
  - `cat << 'INNER_EOF' > test-fixtures/valid-provider-artifact.json`
  - `{"id": "my-artifact", "type": "oci_artifact", "reference": "oci://my-registry/my-artifact:v1", "package_digest": "sha256:e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"}`
  - `INNER_EOF`
  - `bash <path_to_validation_script> test-fixtures/valid-provider-artifact.json`
- **Success Criteria**:
  - The validator command correctly parses the file and exits with code 0 (`[ $? -eq 0 ]`).
- **Edge Cases**:
  - `bash <path_to_validation_script> test-fixtures/invalid-provider-artifact.json` (where type is missing or digest is invalid) should fail (`[ $? -ne 0 ]`).
