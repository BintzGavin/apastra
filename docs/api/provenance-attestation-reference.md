# Provenance Attestation Reference

Schema for supply-chain provenance attestations (SLSA-style).

## Properties

### `attestation_id` (string, Required)
Unique identifier for the attestation.

### `subject` (array[object], Required)
The artifacts that are the subject of the attestation.

### `predicateType` (string, Required)
URI indicating the format of the predicate (e.g., SLSA Provenance).

### `predicate` (object, Required)
The detailed attestation predicate containing builder, invocation, and materials.

