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
        self.assertEqual(results[1], {"assert_invalid": 0.0})
        self.assertEqual(results[2], {"assert_invalid": 0.0})

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


if __name__ == "__main__":
    unittest.main()
