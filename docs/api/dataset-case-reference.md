# Dataset Case Reference

Schema defining a single line of a JSONL dataset for evaluating prompt tests.

## Properties

### `case_id` (string, Required)
Stable identifier for the specific test case.

### `inputs` (object, Required)
Map of variable names to values, mapping to the variables required by the prompt spec.

### `expected_outputs` (object, Optional)
Map of expected output values (e.g., exact matches, substrings).

### `assert` (array[object], Optional)
Array of inline assertions to evaluate the case output against.

### `metadata` (object, Optional)
Arbitrary metadata for the specific test case (e.g., tags, difficulty, domain).

