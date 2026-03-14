import json
import re
import jsonschema

def extract_json_blocks(text):
    """
    Finds potential JSON blocks (objects or arrays) in a string.
    Returns a list of strings that might be JSON.
    Uses a simple brace matching approach.
    """
    blocks = []

    # Try finding markdown code blocks first
    code_blocks = re.findall(r'```(?:json)?\s*(.*?)\s*```', text, re.DOTALL)
    for cb in code_blocks:
        blocks.append(cb)

    # Also try to find raw objects/arrays by matching brackets
    # This is a basic approach, a full parser is complex

    start_indices = []
    for i, char in enumerate(text):
        if char in ('{', '['):
            start_indices.append(i)

    for start in start_indices:
        open_char = text[start]
        close_char = '}' if open_char == '{' else ']'

        count = 0
        in_string = False
        escape = False

        for i in range(start, len(text)):
            char = text[i]

            if escape:
                escape = False
                continue

            if char == '\\':
                escape = True
                continue

            if char == '"':
                in_string = not in_string
                continue

            if not in_string:
                if char == open_char:
                    count += 1
                elif char == close_char:
                    count -= 1

                if count == 0:
                    blocks.append(text[start:i+1])
                    break

    return blocks

def evaluate_assertions(output: str, assertions: list) -> list:
    """
    Evaluates a list of inline assertions against a string output.
    Returns a list of dictionaries with scores: [{"assert_<type>": 1.0 or 0.0}, ...]
    """
    results = []

    if not isinstance(output, str):
        output = str(output)

    for assertion in assertions:
        assert_type = assertion.get("type", "")
        assert_value = assertion.get("value")

        is_negated = False
        base_type = assert_type
        if base_type.startswith("not-"):
            is_negated = True
            base_type = base_type[4:]

        passed = False

        try:
            if base_type == "equals":
                passed = (output == assert_value)
            elif base_type == "contains":
                passed = (assert_value in output)
            elif base_type == "icontains":
                passed = (str(assert_value).lower() in output.lower())
            elif base_type == "contains-any":
                if isinstance(assert_value, list):
                    passed = any(val in output for val in assert_value)
                else:
                    passed = (assert_value in output)
            elif base_type == "contains-all":
                if isinstance(assert_value, list):
                    passed = all(val in output for val in assert_value)
                else:
                    passed = (assert_value in output)
            elif base_type == "regex":
                # Ensure the regex matches anywhere in the string
                passed = bool(re.search(assert_value, output))
            elif base_type == "starts-with":
                passed = output.startswith(assert_value)
            elif base_type == "is-json":
                try:
                    json.loads(output)
                    passed = True
                except ValueError:
                    passed = False
            elif base_type == "contains-json":
                blocks = extract_json_blocks(output)
                for block in blocks:
                    try:
                        json.loads(block)
                        passed = True
                        break
                    except ValueError:
                        continue
            elif base_type == "is-valid-json-schema":
                schema = assert_value
                try:
                    parsed = json.loads(output)
                    jsonschema.validate(instance=parsed, schema=schema)
                    passed = True
                except (ValueError, jsonschema.exceptions.ValidationError):
                    blocks = extract_json_blocks(output)
                    for block in blocks:
                        try:
                            parsed = json.loads(block)
                            jsonschema.validate(instance=parsed, schema=schema)
                            passed = True
                            break
                        except (ValueError, jsonschema.exceptions.ValidationError):
                            continue
            elif base_type in ("similar", "llm-rubric", "factuality", "answer-relevance", "latency", "cost"):
                passed = True
            else:
                # Unknown assertion type, default to fail
                passed = False
        except Exception as e:
            # If assertion logic fails (e.g. invalid regex), it fails
            passed = False

        if is_negated:
            passed = not passed

        results.append({f"assert_{assert_type}": 1.0 if passed else 0.0})

    return results
