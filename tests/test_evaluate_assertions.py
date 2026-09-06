import unittest

from promptops.runs.evaluate_assertions import evaluate_assertions, extract_json_blocks


class EvaluateAssertionsTests(unittest.TestCase):
    def test_malformed_assertions_fail_without_crashing(self):
        results = evaluate_assertions(
            "alpha beta",
            [
                {"type": "contains", "value": "alpha"},
                "not-a-dict",
                {"type": None, "value": "alpha"},
            ],
        )

        self.assertEqual(results[0], {"assert_contains": 1.0})
        self.assertEqual(results[1]["status"], "error")
        self.assertEqual(results[2]["status"], "error")

    def test_contains_any_handles_non_string_values(self):
        results = evaluate_assertions(
            "model selected fallback 42",
            [{"type": "contains-any", "value": [17, 42]}],
        )

        self.assertEqual(results, [{"assert_contains-any": 1.0}])

    def test_extract_json_blocks_handles_fenced_and_inline_json(self):
        blocks = extract_json_blocks(
            'before ```json\n{"from": "fence"}\n``` middle {"inline": [1, 2, 3]} after'
        )

        self.assertIn('{"from": "fence"}', blocks)
        self.assertIn('{"inline": [1, 2, 3]}', blocks)

    def test_model_assisted_assertions_require_a_judge(self):
        for kind in ("llm-rubric", "answer-relevance", "similar", "factuality"):
            with self.subTest(kind=kind):
                result = evaluate_assertions("answer", [{"type": kind, "value": "answer"}])[0]
                self.assertEqual(result.get("status"), "error", result)

    def test_negation_never_turns_an_evaluator_error_into_a_pass(self):
        for kind, value in (("unknown", "x"), ("regex", "["), ("llm-rubric", "x")):
            for prefix in ("", "not-"):
                with self.subTest(kind=prefix + kind):
                    result = evaluate_assertions("x", [{"type": prefix + kind, "value": value}])[0]
                    self.assertEqual(result.get("status"), "error", result)
        self.assertEqual(evaluate_assertions("x", [{"type": "not-contains", "value": "y"}]), [{"assert_not-contains": 1.0}])

    def test_missing_or_invalid_measurements_are_errors_but_measured_zero_is_valid(self):
        for kind in ("cost", "latency"):
            assertion = [{"type": kind, "value": 1}]
            self.assertEqual(evaluate_assertions("", assertion)[0].get("status"), "error")
            for value in (None, -1, "0", True, float("nan"), float("inf")):
                with self.subTest(kind=kind, value=value):
                    self.assertEqual(evaluate_assertions("", assertion, {kind: value})[0].get("status"), "error")
            self.assertEqual(evaluate_assertions("", assertion, {kind: 0}), [{"assert_" + kind: 1.0}])

    def test_judge_results_are_typed_and_exceptions_do_not_trigger_a_second_call(self):
        assertion = [{"type": "similar", "value": "expected", "threshold": 0.8}]
        for value in ("false", None, [], float("nan"), float("inf"), -0.1, 1.1):
            with self.subTest(value=value):
                result = evaluate_assertions("answer", assertion, {"judge_callable": lambda *args: value})[0]
                self.assertEqual(result.get("status"), "error", result)
        self.assertEqual(evaluate_assertions("answer", assertion, {"judge_callable": lambda *args: 0.8}), [{"assert_similar": 1.0}])
        calls = []
        def broken_judge(*args):
            calls.append(args)
            raise TypeError("provider failure")
        result = evaluate_assertions("answer", assertion, {"judge_callable": broken_judge})[0]
        self.assertEqual(result.get("status"), "error")
        self.assertEqual(len(calls), 1)


if __name__ == "__main__":
    unittest.main()
