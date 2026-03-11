#### 1. Context & Goal
- **Objective**: Create a JSON Schema and validation script for `artifact_refs.json`.
- **Trigger**: The README.md "Minimal viable internal schema inventory" requires `artifact_refs.json` (URIs + digests to large raw artifacts). The existing artifacts (run requests, manifests, dataset cases) are defined, but there's a missing link for large payload outputs.
- **Impact**: Unlocks the EVALUATION domain's ability to store and refer to large, raw test artifacts securely via verifiable content digests without bloating the git history or `cases.jsonl` files.

#### 2. File Inventory
- **Create**:
  - `promptops/schemas/artifact-refs.schema.json`
  - `promptops/validators/validate-artifact-refs.sh`
- **Modify**: None
- **Read-Only**: `README.md`

#### 3. Implementation Spec
- **Schema Architecture**:
  - Format: JSON Schema (Draft 2020-12)
  - Expected structure: A root object containing an array of object references or mapping stable reference IDs to object metadata.
  - Required fields per reference object: `uri` (string URI to the location of the raw artifact), `digest` (string SHA-256 digest matching `^sha256:[a-f0-9]{64}$`).
  - Optional fields: `mime_type` (string).
- **Content Digest Convention**:
  - The digests listed within `artifact_refs.json` must be computed by the artifact producer over the raw bytes of the file being stored at the `uri` using SHA-256.
- **Pseudo-Code**:
  - `validate-artifact-refs.sh` will receive a JSON file path as input.
  - It will run `npx ajv-cli validate -s promptops/schemas/artifact-refs.schema.json -d "$1" --spec=draft2020 --strict=false`
  - Exit with success if valid, fail if not.
- **Public Contract Changes**: Exports `https://apastra.com/schemas/promptops/artifact-refs.schema.json` schema.
- **Dependencies**: None.

#### 4. Test Plan
- **Verification**:
  ```bash
  mkdir -p test-fixtures
  cat << 'EOF' > test-fixtures/valid-artifact-refs.json
  {
    "references": {
      "raw-response-1": {
        "uri": "s3://my-bucket/run-123/raw-1.json",
        "digest": "sha256:e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
        "mime_type": "application/json"
      }
    }
  }
  EOF
  cat << 'EOF' > test-fixtures/invalid-artifact-refs.json
  {
    "references": {
      "raw-response-1": {
        "uri": "s3://my-bucket/run-123/raw-1.json",
        "digest": "md5:12345"
      }
    }
  }
  EOF
  chmod +x promptops/validators/validate-artifact-refs.sh
  ./promptops/validators/validate-artifact-refs.sh test-fixtures/valid-artifact-refs.json
  [ $? -eq 0 ] || exit 1
  ./promptops/validators/validate-artifact-refs.sh test-fixtures/invalid-artifact-refs.json
  [ $? -ne 0 ] || exit 1
  rm -f test-fixtures/valid-artifact-refs.json test-fixtures/invalid-artifact-refs.json
  ```
- **Success Criteria**: Validation succeeds for correctly formed references (proper URI and `sha256:` digest format) and fails when a digest doesn't match the required regex.
- **Edge Cases**: Empty references object, missing required `uri` or `digest` keys, incorrect digest formatting (e.g. `md5:`).