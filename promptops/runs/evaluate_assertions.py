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

class AssertionEvaluationError(ValueError):
    pass


def _invalid_json_constant(_value):
    raise ValueError("Nonfinite JSON")


def _number(value):
    import math
    return type(value) in (int, float) and math.isfinite(value)


def _evaluate(output, assertion, metadata):
    kind = assertion["type"].removeprefix("not-")
    value = assertion.get("value")
    if kind not in ("is-json", "contains-json") and "value" not in assertion:
        raise AssertionEvaluationError("missing_assertion_value")
    if kind == "equals":
        return output == value
    if kind in ("contains", "icontains"):
        return str(value) in output if kind == "contains" else str(value).lower() in output.lower()
    if kind in ("contains-any", "contains-all"):
        values = value if isinstance(value, list) else [value]
        if not values:
            raise AssertionEvaluationError("empty_assertion_values")
        matches = (str(item) in output for item in values)
        return any(matches) if kind == "contains-any" else all(matches)
    if kind == "regex":
        return bool(re.search(value, output))
    if kind == "starts-with":
        return output.startswith(value)
    if kind in ("is-json", "contains-json", "is-valid-json-schema"):
        if kind == "is-valid-json-schema":
            jsonschema.Draft202012Validator.check_schema(value)
        candidates = [output] if kind == "is-json" else [output, *extract_json_blocks(output)]
        for candidate in candidates:
            try:
                parsed = json.loads(candidate, parse_constant=_invalid_json_constant)
                if kind == "is-valid-json-schema":
                    jsonschema.validate(parsed, value)
                return True
            except (ValueError, jsonschema.ValidationError):
                continue
        return False
    if kind in ("cost", "latency"):
        measured = metadata.get(kind)
        if not _number(measured) or measured < 0:
            raise AssertionEvaluationError("missing_or_invalid_measurement")
        if not _number(value) or value < 0:
            raise AssertionEvaluationError("invalid_measurement_threshold")
        return measured <= value
    if kind in ("llm-rubric", "answer-relevance", "similar", "factuality"):
        judge = metadata.get("judge_callable")
        if not callable(judge):
            raise AssertionEvaluationError("judge_required")
        threshold = assertion.get("threshold", 0.8)
        reference = value
        if kind == "similar" and isinstance(value, dict):
            threshold = value.get("threshold", threshold)
            reference = value.get("value")
        if not reference or not _number(threshold) or not 0 <= threshold <= 1:
            raise AssertionEvaluationError("invalid_judge_configuration")
        # One invocation; a provider TypeError must not trigger a second paid call.
        score = judge(output, reference)
        if type(score) is bool:
            return score
        if not _number(score) or not 0 <= score <= 1:
            raise AssertionEvaluationError("invalid_judge_result")
        return score >= threshold
    raise AssertionEvaluationError("unsupported_assertion")


def evaluate_assertions(output: str, assertions: list, metadata: dict = None) -> list:
    """Return numeric verdicts, or explicit errors with no numeric score."""
    if not isinstance(assertions, list):
        raise ValueError("Assertions must be a list")
    results = []
    for assertion in assertions:
        kind = assertion.get("type") if isinstance(assertion, dict) else None
        if not isinstance(kind, str) or not kind:
            results.append({"status": "error", "reason": "invalid_assertion"})
            continue
        try:
            passed = _evaluate(str(output), assertion, metadata or {})
        except Exception as error:
            reason = str(error) if isinstance(error, AssertionEvaluationError) else "evaluator_error"
            results.append({"status": "error", "assertion": kind, "reason": reason})
            continue
        if kind.startswith("not-"):
            passed = not passed
        results.append({"assert_" + kind: 1.0 if passed else 0.0})
    return results


def main():
    import argparse
    from pathlib import Path
    import sys

    parser = argparse.ArgumentParser(description="Evaluate inline assertions; errors never score as passes.")
    parser.add_argument("output_file")
    parser.add_argument("assertions_file")
    parser.add_argument("metadata_file", nargs="?")
    args = parser.parse_args()
    try:
        results = evaluate_assertions(
            Path(args.output_file).read_text(encoding="utf-8"),
            json.loads(Path(args.assertions_file).read_text(encoding="utf-8")),
            json.loads(Path(args.metadata_file).read_text(encoding="utf-8")) if args.metadata_file else {},
        )
    except (OSError, ValueError, TypeError):
        print(json.dumps({"status": "error", "reason": "invalid_assertion_input"}), file=sys.stderr)
        return 1
    print(json.dumps(results, indent=2, allow_nan=False))
    if not results or any(row.get("status") == "error" for row in results):
        return 1
    return 0 if all(all(value == 1.0 for value in row.values()) for row in results) else 2


if __name__ == "__main__":
    raise SystemExit(main())
