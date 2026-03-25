---
title: "Digest Convention Reference"
description: "Content Digest Convention for Apastra assets"
audience: "developers | platform-teams"
last_verified: "2026-03-25"
source_files:
  - "promptops/schemas/digest-convention.md"
---

# Digest Convention Reference

Define the "Content-digest convention" spec detailing how content digests are computed and represented for apastra PromptOps assets. This unlocks Git-first resolution, durable inputs for harness adapters (EVALUATION), and provenance metadata for tracking artifacts across environments.

## Convention Specs

### Canonicalization Rules

1. **JSON Files (`.json`)**:
   - The JSON content must be canonicalized.
   - Keys must be sorted alphabetically.
   - All insignificant whitespace (spaces, tabs, newlines outside of string values) must be removed.
   - Canonicalization should be equivalent to running `jq -cSM . <file>`.

2. **YAML Files (`.yaml`, `.yml`)**:
   - The YAML content must first be converted into a JSON object.
   - Once converted, the resulting JSON must follow the same canonicalization rules as JSON files.

3. **JSONL Files (`.jsonl`)**:
   - For JSON Lines files, each individual line must be parsed as JSON and canonicalized independently according to the JSON canonicalization rules.
   - The canonicalized lines must then be rejoined using exactly one newline character (`\n`) between each line.
   - Ensure the final joined string is used for digest computation.

### Digest Computation

- The canonicalized string representation of the file (JSON, YAML converted to JSON, or JSONL) is hashed using the **SHA-256** algorithm.
- The resulting digest must be formatted as a string with the `sha256:` prefix followed by the hexadecimal representation of the hash.
  - Example: `sha256:e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`

### Storage

- The `digest` field in all schemas (such as dataset manifests, run artifacts, etc.) must store this exact formatted string.
