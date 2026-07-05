import os
import tempfile
import unittest
from pathlib import Path

from promptops.resolver.workspace import WorkspaceResolver


class WorkspaceResolverTests(unittest.TestCase):
    def test_rejects_prompt_id_path_traversal(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "promptops").mkdir()
            (root / "promptops" / "secrets.yaml").write_text(
                "id: secrets\ntemplate: leaked\n",
                encoding="utf-8",
            )

            previous = os.getcwd()
            os.chdir(root)
            try:
                with self.assertRaises(ValueError):
                    WorkspaceResolver().resolve("../secrets")
            finally:
                os.chdir(previous)

    def test_resolves_quick_eval_from_minimal_workspace(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "evals").mkdir()
            (root / "evals" / "summarize.yaml").write_text(
                "id: summarize\nprompt: 'Summarize {{text}}'\n",
                encoding="utf-8",
            )

            previous = os.getcwd()
            os.chdir(root)
            try:
                resolved = WorkspaceResolver().resolve("summarize")
            finally:
                os.chdir(previous)

        self.assertEqual(
            resolved,
            {
                "id": "summarize",
                "template": "Summarize {{text}}",
                "variables": {},
            },
        )


if __name__ == "__main__":
    unittest.main()
