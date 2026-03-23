# harness-adapter Reference

## Properties

### `id` (string, Required)
Stable identifier for the harness adapter.

### `type` (string, Required)
Must be 'harness_adapter'.

### `capabilities` (array[string], Required)
List of capabilities (e.g., ['run_suite', 'trials', 'model_matrix']).

### `entrypoint` (string, Required)
The CLI command or script to invoke the harness.

### `description` (string, Optional)
Optional description of the harness adapter.

### `env_vars` (array[string], Optional)
Required environment variables (e.g., 'OPENAI_API_KEY').

### `digest` (string, Optional)
Content digest stored inline.

