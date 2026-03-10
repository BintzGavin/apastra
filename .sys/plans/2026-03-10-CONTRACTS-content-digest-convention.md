#### 1. Context & Goal
- **Objective**: Define the "Content-digest convention" spec detailing how content digests are computed and represented for apastra PromptOps assets.
- **Trigger**: The README.md requires content digests for all immutable assets (prompt specs, dataset cases, run artifacts, etc.) to ensure reproducibility, provenance, and to guarantee "what exactly ran" and "what exactly shipped" (Phase 1: Deterministic digest tooling).
- **Impact**: This unlocks Git-first resolution, durable inputs for harness adapters (EVALUATION), and provenance metadata for tracking artifacts across environments. It provides the foundation for immutable releases and secure, content-addressed references.

#### 2. File Inventory
- **Create**:
  - `promptops/schemas/digest-convention.md` (A document fully specifying the canonicalization and digest rules)
  - `promptops/validators/compute-digest.sh` (A script implementing the canonicalization and digest computation)
- **Modify**: []
- **Read-Only**:
  - `README.md`
  - `promptops/schemas/prompt-spec.schema.json`
  - `promptops/schemas/dataset-manifest.schema.json`
  - `promptops/schemas/dataset-case.schema.json`
  - `promptops/schemas/evaluator.schema.json`
  - `promptops/schemas/suite.schema.json`

#### 3. Implementation Spec
- **Schema Architecture**:
  - The convention requires that any given promptops JSON or YAML asset is first normalized into canonical JSON (e.g., following RFC 8785) before hashing.
  - The format for storing the digest must be a string starting with the hash algorithm prefix, e.g., `sha256:<hex>`.
  - For YAML files, they must be converted to canonical JSON before hashing so that `foo.yaml` and `foo.json` representing the same object yield the same digest.
  - For JSONL files (like `cases.jsonl`), the digest is computed over the entire file exactly as is, or by normalizing each line to canonical JSON and joining with newlines, then hashing. (The spec must explicitly decide this rule; standardizing on hashing the exact bytes of the `cases.jsonl` file is recommended for simplicity, or canonicalizing line-by-line if JSON formatting variance is expected).
- **Content Digest Convention**:
  - The `digest` field in schemas (like dataset manifest) holds the `sha256:<hex>` representation.
  - Computation: `echo -n <canonical_json> | sha256sum | awk '{print "sha256:"$1}'`.
- **Pseudo-Code**:
  - `compute-digest(file)`:
    1. Read the input `file`.
    2. If `file` is JSON or YAML, parse the content into an object.
    3. Serialize the object into canonical JSON (e.g., sort object keys, remove insignificant whitespace).
    4. Compute the SHA-256 hash of the canonical JSON string.
    5. Return `sha256:<hash>`.
    6. If `file` is JSONL, process each line or the raw file as defined by the spec, compute SHA-256, and return the prefixed hash.
- **Public Contract Changes**:
  - Introduce standard `digest` format `sha256:<hex>` expected by all systems.
- **Dependencies**:
  - None.

#### 4. Test Plan
- **Verification**:
  - Run the `compute-digest.sh` on two logically identical files (e.g., `valid-prompt-spec.json` and a rearranged or YAML equivalent like `valid-prompt-spec.yaml`).
  - Example command: `./promptops/validators/compute-digest.sh test-fixtures/valid-prompt-spec.json` and `./promptops/validators/compute-digest.sh test-fixtures/valid-prompt-spec.yaml`
- **Success Criteria**:
  - The script outputs the exact same `sha256:<hex>` string for both the JSON and YAML versions of the same asset.
- **Edge Cases**:
  - Files with different key orders must yield the same digest.
  - Files with extra whitespace must yield the same digest.
  - Invalid JSON/YAML files should cause the script to exit with an error.