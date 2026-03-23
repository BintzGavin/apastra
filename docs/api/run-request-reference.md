# Run Request Specification Reference

Schema for a minimal BYO harness run request.

## Properties

### `suite_id` (string, Required)
The benchmark suite ID

### `revision_ref` (string, Required)
The revision ref (SHA/tag/digest)

### `model_matrix` (array[string], Required)
Model matrix

### `evaluator_refs` (array[string], Required)
Evaluator references

### `trials` (integer, Optional)
Number of trials

### `budgets` (object, Optional)
Budgets

### `timeouts` (object, Optional)
Timeouts

### `artifact_backend_config` (object, Optional)
Artifact backend config

