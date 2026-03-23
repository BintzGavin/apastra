# Quick Eval Reference

Schema defining a combined quick evaluation file containing prompt, cases, and assertions.

## Properties

### `id` (string, Required)
Stable identifier for the quick eval.

### `prompt` (string, Required)
The prompt template.

### `cases` (array[ref https://promptops.apastra.com/schemas/dataset-case.schema.json], Required)
Array of dataset cases with inputs and inline asserts.

### `thresholds` (object, Optional)
Optional thresholds for the evaluation.

