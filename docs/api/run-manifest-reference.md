# Run Manifest Specification Reference

Schema for a run manifest.

## Properties

### `input_refs` (object, Required)
Input references

### `resolved_digests` (object, Required)
Resolved digests

### `timestamps` (object, Required)
Timestamps

### `harness_identifier` (string, Required)
Harness identifier

### `harness_version` (string, Required)
Harness version

### `model_ids` (array[string], Required)
Model IDs

### `sampling_config` (object, Required)
Sampling configuration

### `environment` (object, Required)
Environment metadata

### `status` (string, Required)
Run status

### `provenance` (object, Optional)
SLSA-style provenance metadata representing the invocation of the evaluation run.

