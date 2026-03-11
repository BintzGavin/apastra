#### 1. Context & Goal
- **Objective**: Implement deterministic digest computation tooling for prompt specs and datasets.
- **Trigger**: The README.md "Phased build plan" requires "Deterministic digest tooling" as Phase 3 to enable reproducibility and meaningful lineage.
- **Impact**: Unlocks Git-first resolution, durable inputs for harness adapters (EVALUATION), and provenance metadata for tracking artifacts across environments by providing a canonical identity for content.

#### 2. File Inventory
- **Create**: [A python module containing functions to compute content digests for JSON, YAML, and JSONL formats]
- **Create**: [A CLI script for generating digests easily from the terminal]
- **Modify**: `promptops/runtime/resolve.py` (Update `compute_digest` to import and use the new dedicated digest functions)
- **Read-Only**: `promptops/schemas/digest-convention.md`, `README.md`

#### 3. Implementation Spec
- **Architecture**: Create a standalone python module responsible for taking file paths or parsed data structures and producing canonical JSON strings (using `json.dumps(obj, separators=(',', ':'), sort_keys=True)` or `jq -cSM .` semantics) and hashing them using SHA-256.
- **Formats**:
    - JSON: load, canonicalize, hash.
    - YAML: load (using `pyyaml`), canonicalize to JSON, hash.
    - JSONL: process line-by-line, parsing each line as JSON, canonicalizing it, re-joining with exactly one newline `\n`, then hashing the entire block.
- **Output Format**: Ensure all outputs strictly return strings starting with `sha256:` followed by the hex digest.
- **Dependencies**: Depends on the existing `promptops/schemas/digest-convention.md` specification. No unmet dependencies.

#### 4. Test Plan
- **Verification**: `echo '{"b": 2, "a": 1}' | jq -cSM . | sha256sum | awk '{print "sha256:" $1}' > test_hash.txt && cat test_hash.txt | grep "sha256:4d45dc7168db709121ebbb5697699d75b0fb609dc696dbf583ed8357a7da0da7"`
- **Success Criteria**: `[ $? -eq 0 ]`
- **Edge Cases**:
  - `echo '{"a": {"c": 3, "b": 2}}' | jq -cSM . | sha256sum | awk '{print "sha256:" $1}' > test_nested.txt && [ -s test_nested.txt ]`
  - `echo -e '{"a": 1}\n{"b": 2}\n' > test_jsonl.txt && cat test_jsonl.txt | while read line; do [ -z "$line" ] && continue; echo "$line" | jq -cSM .; done | sha256sum | awk '{print "sha256:" $1}' > test_jsonl_hash.txt && [ -s test_jsonl_hash.txt ]`
  - `rm -f test_hash.txt test_nested.txt test_jsonl.txt test_jsonl_hash.txt`
