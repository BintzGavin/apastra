#### 1. Context & Goal
- **Objective**: Implement deterministic digest computation for prompts and datasets to ensure reproducibility.
- **Trigger**: The README.md specifies "Deterministic digest tooling: Canonicalization + digests for prompts/datasets" as part of the repo build handoff.
- **Impact**: Enables stable canonical identity for prompt specs and dataset cases, allowing robust cache lookup and integrity verification for all consuming domains.

#### 2. File Inventory
- **Create**: `promptops/runtime/digest.py` (Script to canonicalize and hash JSON/YAML/JSONL)
- **Modify**: `promptops/runtime/resolve.py` (to use the new digest module)
- **Read-Only**: `promptops/schemas/digest-convention.md`

#### 3. Implementation Spec
- **Resolver Architecture**: The digest computation logic ensures identical contents yield identical hashes. Files are loaded, canonicalized (JSON sorted keys, no whitespace), and hashed via SHA-256.
- **Manifest Format**: Not applicable.
- **Pseudo-Code**:
  1. If file is YAML, convert to dict using `yaml.safe_load`.
  2. If file is JSON, load as dict.
  3. If file is JSONL, read line by line.
  4. For dicts, dump with `json.dumps(obj, separators=(',', ':'), sort_keys=True)`.
  5. For JSONL, dump each line as canonical JSON and join with newlines.
  6. Hash the canonicalized byte string using `hashlib.sha256()`.
  7. Return `sha256:<hex>`.
- **Harness Contract Interface**: Not applicable.
- **Dependencies**: CONTRACTS `promptops/schemas/digest-convention.md`.

#### 4. Test Plan
- **Verification**: `mkdir -p test-fixtures && echo 'a: 1' > test-fixtures/sample.yaml && python promptops/runtime/digest.py test-fixtures/sample.yaml`
- **Success Criteria**: `[ $? -eq 0 ]`
- **Edge Cases**: `mkdir -p test-fixtures && touch test-fixtures/empty.yaml && python promptops/runtime/digest.py test-fixtures/empty.yaml; [ $? -ne 0 ]`
