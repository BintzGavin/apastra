#### 1. Context & Goal
- **Objective**: Implement the `is-valid-json-schema` assertion type for inline evaluation.
- **Trigger**: The docs/vision.md and README.md define `is-valid-json-schema` as a built-in deterministic assertion type, but `promptops/runs/evaluate_assertions.py` lacks this implementation, causing such assertions to silently fail.
- **Impact**: Unlocks deterministic validation of LLM JSON outputs against predefined schemas, a critical capability for reliable tool-calling and structured data extraction.

#### 2. File Inventory
- **Create**: None
- **Modify**: `promptops/runs/evaluate_assertions.py` - Add logic to validate `is-valid-json-schema` using the `jsonschema` library.
- **Read-Only**: `promptops/schemas/dataset-case.schema.json`, `docs/vision.md`

#### 3. Implementation Spec
- **Harness Architecture**: N/A (Inline assertions logic)
- **Run Request Format**: N/A
- **Run Artifact Format**: N/A
- **Pseudo-Code**:
  - In `evaluate_assertions.py`, import `jsonschema` (and potentially `json`).
  - Add an `elif base_type == "is-valid-json-schema":` block in the evaluation loop.
  - If the output itself is valid JSON and matches the schema (which is passed in `assert_value`), pass the assertion.
  - If the output is not strictly JSON, use `extract_json_blocks(output)` to find potential JSON substrings. Check if any extracted block is valid JSON and matches the provided schema using `jsonschema.validate`. If at least one matches, pass the assertion.
  - Catch validation exceptions (`jsonschema.exceptions.ValidationError`, `json.JSONDecodeError`) and mark as failed.
- **Baseline and Regression Flow**: N/A
- **Dependencies**: CONTRACTS schemas required (`dataset-case.schema.json`); RUNTIME resolver availability; `jsonschema` Python package must be installed in the evaluation environment.

#### 4. Test Plan
- **Verification**: `python3 -c "import sys; sys.path.insert(0, 'promptops/runs'); from evaluate_assertions import evaluate_assertions; assert evaluate_assertions('{\"a\": 1}', [{'type': 'is-valid-json-schema', 'value': {'type': 'object', 'properties': {'a': {'type': 'integer'}}}}])[0]['assert_is-valid-json-schema'] == 1.0; print('Assertion passed')"`
- **Success Criteria**: A run utilizing `is-valid-json-schema` correctly passes when output matches the schema and fails when it doesn't.
- **Edge Cases**: The model outputs preamble text before the JSON block; the model outputs markdown code blocks enclosing the JSON; the schema itself is invalid.
