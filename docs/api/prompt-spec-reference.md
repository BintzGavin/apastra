# Prompt Specification Reference

Source-of-truth prompt definition with a stable ID, variable schema, output contract, and metadata.

## Properties

### `id` (string, Required)
Stable identifier for the prompt (e.g., 'my-app/summarize-v1').

### `variables` (object, Required)
Map of variable names to their JSON Schema types (e.g., {'text': {'type': 'string'}}).

### `template` (['string', 'object', 'array'], Required)
The prompt template content (e.g., Jinja2 string, or array of message objects for chat models).

### `output_contract` (object, Optional)
JSON Schema defining the expected output structure from the model.

### `metadata` (object, Optional)
Arbitrary key-value pairs (e.g., author, intent, tags).

### `tool_contract` (object, Optional)
JSON Schema defining the expected tool calling structure and available tools.

