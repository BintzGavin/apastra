import tempfile
import unittest
from pathlib import Path

from promptops.resolver.git_ref import GitRefResolver
from promptops.resolver.local import LocalResolver


class ResolverSafetyTests(unittest.TestCase):
    def test_local_resolver_rejects_prompt_id_path_traversal(self):
        with tempfile.TemporaryDirectory() as tmp:
            prompt_path = Path(tmp) / "prompt.yaml"
            prompt_path.write_text("id: demo\ntemplate: hi\n", encoding="utf-8")

            with self.assertRaises(ValueError):
                LocalResolver().resolve("../secret", str(prompt_path))

    def test_git_ref_directory_reader_rejects_prompt_id_path_traversal(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "promptops").mkdir()
            (root / "promptops" / "secret.yaml").write_text(
                "id: secret\ntemplate: leaked\n",
                encoding="utf-8",
            )

            with self.assertRaises(ValueError):
                GitRefResolver()._read_from_dir(str(root), "../secret")


if __name__ == "__main__":
    unittest.main()
