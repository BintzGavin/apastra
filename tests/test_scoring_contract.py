import unittest

from promptops.runs.normalize import normalize_scorecard


DEFINITIONS = {"accuracy": {"version": "1", "unit": "ratio", "direction": "higher_is_better"}}


class NormalizationTests(unittest.TestCase):
    def test_incomplete_or_error_rows_cannot_improve_the_mean(self):
        for rows in ([], [{"case_id": "one", "evaluator_outputs": [{"status": "error"}]}],
                     [{"case_id": "one", "evaluator_outputs": [{"accuracy": 1}, {}]}]):
            with self.subTest(rows=rows), self.assertRaises(ValueError):
                normalize_scorecard(rows)

    def test_explicit_definitions_and_complete_trial_scores_are_required(self):
        cases = [{"case_id": "one", "model_id": "target", "per_trial_outputs": [
            {"trial_id": 1, "output": "a", "evaluator_outputs": {"accuracy": 0}},
            {"trial_id": 2, "output": "b", "evaluator_outputs": {"accuracy": 1}},
        ]}]
        scorecard = normalize_scorecard(cases, DEFINITIONS)
        self.assertEqual(scorecard["normalized_metrics"], {"accuracy": 0.5})
        self.assertEqual(scorecard["variance"], {"accuracy": 0.25})
        self.assertEqual(scorecard["metric_definitions"], DEFINITIONS)
        cases[0]["per_trial_outputs"][1]["evaluator_outputs"] = {"status": "error"}
        with self.assertRaises(ValueError):
            normalize_scorecard(cases, DEFINITIONS)
