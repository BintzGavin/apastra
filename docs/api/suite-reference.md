# Benchmark Suite Specification Reference

Benchmark suite declaring datasets, evaluators, model/provider matrix, trials, budgets, and thresholds.

## Properties

### `id` (string, Required)
Stable identifier for the suite.

### `name` (string, Required)
Human-readable name of the suite.

### `description` (string, Optional)
Optional detailed description of the suite's purpose.

### `datasets` (array[string], Required)
Array of dataset references.

### `evaluators` (array[string], Required)
Array of evaluator references.

### `model_matrix` (array[string], Required)
Array of model/provider identifiers to run the suite against.

### `trials` (integer, Optional)
Number of times to run the evaluation.

### `budgets` (object, Optional)
Cost or time limits for the execution.

### `thresholds` (object, Optional)
Pass/fail criteria mapped to specific metrics.

