import json
import re
import jsonschema

def extract_json_blocks(text):
    """
    Finds potential JSON blocks (objects or arrays) in a string.
    Returns a list of strings that might be JSON.
    Uses JSONDecoder so braces in prose do not create false positives.
    """
    if not isinstance(text, str):
        text = str(text)

    blocks = []
    seen = set()

    code_blocks = re.findall(r'```(?:json)?\s*(.*?)\s*```', text, re.DOTALL)
    for cb in code_blocks:
        candidate = cb.strip()
        if candidate and candidate not in seen:
            blocks.append(candidate)
            seen.add(candidate)

    decoder = json.JSONDecoder()
    for start, char in enumerate(text):
        if char not in ("{", "["):
            continue
        try:
            _, end = decoder.raw_decode(text[start:])
        except ValueError:
            continue
        candidate = text[start:start + end]
        if candidate not in seen:
            blocks.append(candidate)
            seen.add(candidate)

    return blocks

def _invalid_assertion_result():
    return {"assert_invalid": 0.0}

def _contains_value(output, value):
    return str(value) in output

def evaluate_assertions(output: str, assertions: list, metadata: dict = None) -> list:
    """
    Evaluates a list of inline assertions against a string output.
    Returns a list of dictionaries with scores: [{"assert_<type>": 1.0 or 0.0}, ...]
    """
    if metadata is None:
        metadata = {}
    results = []

    if not isinstance(output, str):
        output = str(output)

    for assertion in assertions:
        if not isinstance(assertion, dict):
            results.append(_invalid_assertion_result())
            continue

        assert_type = assertion.get("type", "")
        if not isinstance(assert_type, str) or not assert_type:
            results.append(_invalid_assertion_result())
            continue

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
                passed = _contains_value(output, assert_value)
            elif base_type == "icontains":
                passed = (str(assert_value).lower() in output.lower())
            elif base_type == "contains-any":
                if isinstance(assert_value, list):
                    passed = any(_contains_value(output, val) for val in assert_value)
                else:
                    passed = _contains_value(output, assert_value)
            elif base_type == "contains-all":
                if isinstance(assert_value, list):
                    passed = all(_contains_value(output, val) for val in assert_value)
                else:
                    passed = _contains_value(output, assert_value)
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
            elif base_type == "latency":
                passed = float(metadata.get("latency", 0)) <= float(assert_value)
            elif base_type == "cost":
                passed = float(metadata.get("cost", 0.0)) <= float(assert_value)
            elif base_type in ("answer-relevance", "llm-rubric"):
                if "judge_callable" in metadata:
                    passed = metadata["judge_callable"](output, assert_value)
                elif assert_value:
                    if isinstance(assert_value, list):
                        passed = all(str(v).lower() in output.lower() for v in assert_value)
                    else:
                        passed = str(assert_value).lower() in output.lower()
                else:
                    passed = True
            elif base_type == "similar":
                threshold = assertion.get("threshold", 0.8)
                reference = assert_value
                if isinstance(assert_value, dict):
                    threshold = assert_value.get("threshold", threshold)
                    reference = assert_value.get("value", "")

                if "judge_callable" in metadata:
                    try:
                        score = metadata["judge_callable"](output, reference, type="similar")
                    except TypeError:
                        score = metadata["judge_callable"](output, reference)
                    if isinstance(score, bool):
                        passed = score
                    else:
                        try:
                            passed = float(score) >= float(threshold)
                        except (ValueError, TypeError):
                            passed = bool(score)
                else:
                    passed = str(reference).lower() in output.lower()
            elif base_type == "factuality":
                if "judge_callable" in metadata:
                    try:
                        score = metadata["judge_callable"](output, assert_value, type="factuality")
                    except TypeError:
                        score = metadata["judge_callable"](output, assert_value)
                    passed = bool(score)
                else:
                    if isinstance(assert_value, list):
                        passed = all(str(v).lower() in output.lower() for v in assert_value)
                    else:
                        passed = str(assert_value).lower() in output.lower()
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


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 3:
        print("Usage: python evaluate_assertions.py <output_text_file> <assertions.json> [metadata.json]")
        print("  output_text_file: file containing the model output text")
        print("  assertions.json:  JSON array of assertion objects")
        print("  metadata.json:    optional JSON object with latency, cost, etc.")
        sys.exit(1)

    with open(sys.argv[1], 'r') as f:
        output_text = f.read()

    with open(sys.argv[2], 'r') as f:
        assertions = json.load(f)

    metadata = {}
    if len(sys.argv) >= 4:
        with open(sys.argv[3], 'r') as f:
            metadata = json.load(f)

    results = evaluate_assertions(output_text, assertions, metadata)
    print(json.dumps(results, indent=2))
