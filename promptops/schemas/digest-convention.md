# Content digest convention, version 2

The Python implementation in `runtime/digest.py` is the normative implementation.
The CLI, shell digest helper, suite resolution, MCP, and comparison use it.

Structured files contain JSON-compatible values. JSON and YAML keys must be
unique strings. Reject nonfinite numbers and YAML values that cannot be
represented in JSON, including timestamp objects.

Canonicalize objects by sorting keys and removing insignificant whitespace.
Encode strings as UTF-8 without ASCII escaping. Integral floating-point values,
including negative zero, canonicalize as integers. Booleans remain distinct from
numbers. Other finite floats use Python's JSON numeric representation.

For JSONL, canonicalize each nonblank line and join the rows using exactly one
newline between rows, without a trailing newline. Row order is significant.
An empty file has a digest but is not a valid evaluation dataset.

Compute SHA-256 over the canonical UTF-8 bytes and prefix its lowercase hex
representation with `sha256:`.

For multiple datasets or evaluators, first compute each individual digest in
the order declared by the suite. A single asset retains its individual digest.
For two or more assets, hash the canonical object:

```json
{"domain":"apastra:asset-group:v2","kind":"datasets","digests":["sha256:...","sha256:..."]}
```

Use `evaluators` as the kind for evaluator groups. This domain and ordered digest
list preserve group boundaries. Embedded dataset snapshots use the same JSONL
rule as source files.

## Fixed vector

These documents have identical canonical bytes, `{"a":1,"b":"é"}`:

```json
{"b":"é","a":1.0}
```

```yaml
a: 1
b: é
```

Expected digest:

```text
sha256:09ad9fd2fb648cb2f62141215828ea00a62c299db05d20aa9ade2f527a301cc6
```

Version 1 examples based on raw YAML, ASCII-escaped JSON, or reference names
cannot be treated as version 2 evidence. Retain them as historical records and
recompute identities when producing a new run.

Dataset manifest digests identify the corresponding cases file. Package identity
is computed externally over the complete package document, which avoids a
self-referential digest requirement. Extra artifact references identify raw file
bytes rather than structured semantic content.
