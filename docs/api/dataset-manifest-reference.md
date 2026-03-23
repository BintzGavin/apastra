# Dataset Manifest Reference

Schema for a dataset manifest, defining identity, version, schema version, digest, and provenance.

## Properties

### `id` (string, Required)
Stable identifier for the dataset.

### `version` (string, Required)
Semantic version or revision of the dataset.

### `digest` (string, Required)
Content digest (e.g., SHA-256) of the associated dataset.jsonl file to ensure reproducibility.

### `schema_version` (string, Required)
Version of the dataset case schema used by the JSONL file.

### `provenance` (object, Optional)
Information about the origin and creation of the dataset.

