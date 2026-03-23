# Evaluator Specification Reference

Scoring definition (deterministic checks, schema validation, rubric/judge config)

## Properties

### `id` (string, Required)
Stable identifier for the evaluator.

### `type` (string, Required)
The type of the evaluator.
**Enum values:** deterministic, schema, judge, human

### `metrics` (array[string], Required)
Array of metrics produced by this evaluator.

### `description` (string, Optional)
Optional human-readable description of the evaluator.

### `config` (object, Optional)
Configuration specific to the evaluator type, such as model details or target values.

### `metric_versions` (object, Optional)
Mapping of metric names to their semantic versions.

### `digest` (string, Optional)
SHA-256 hash of the evaluator content.

