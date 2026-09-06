from pathlib import Path
import tempfile
import unittest

from promptops.runtime.digest import compute_digest


class DigestContractTests(unittest.TestCase):
    def test_json_yaml_and_numeric_formatting_share_one_fixed_identity(self):
        with tempfile.TemporaryDirectory() as directory:
            actual = []
            for name, content in (("one.json", '{"b":"é", "a":1.0}'), ("two.yaml", "a: 1\nb: é\n")):
                path = Path(directory) / name
                path.write_text(content)
                actual.append(compute_digest(str(path)))
            self.assertEqual(actual[0], actual[1])
            self.assertEqual(actual[0], "sha256:09ad9fd2fb648cb2f62141215828ea00a62c299db05d20aa9ade2f527a301cc6")

    def test_duplicate_keys_and_nonfinite_values_are_not_hashable_assets(self):
        with tempfile.TemporaryDirectory() as directory:
            for name, content in (("duplicate.json", '{"a":1,"a":2}'), ("duplicate.yaml", "a: 1\na: 2\n"), ("nan.json", '{"a":NaN}'), ("nan.yaml", "a: .nan\n")):
                with self.subTest(name=name):
                    path = Path(directory) / name
                    path.write_text(content)
                    with self.assertRaises(ValueError):
                        compute_digest(str(path))
