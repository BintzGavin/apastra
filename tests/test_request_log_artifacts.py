import json
import hashlib
import os
import stat
import tempfile
import time
import unittest
from datetime import datetime, timezone
from pathlib import Path

from promptops.request_log.artifacts import RequestArtifactStore


class RequestArtifactStoreTests(unittest.TestCase):
    def test_writes_exact_bytes_and_safe_metadata_with_private_permissions(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir) / "logs"
            store = RequestArtifactStore(root)
            body = b'{ "model": "gpt-test", "input": [{"role":"user","content":"secret body"}] }\n'

            artifact = store.begin_request(
                provider="openai",
                adapter="codex",
                method="POST",
                request_path="/v1/responses?api_key=must-not-appear",
                content_type="application/json",
                body=body,
            )
            store.complete_request(artifact.request_id, status=200, duration_ms=12)

            self.assertEqual(artifact.body_path.read_bytes(), body)
            metadata = json.loads(artifact.metadata_path.read_text())
            self.assertEqual(
                set(metadata),
                {
                    "schema_version",
                    "request_id",
                    "timestamp",
                    "provider",
                    "adapter",
                    "method",
                    "path",
                    "content_type",
                    "body_bytes",
                    "body_sha256",
                    "response_status",
                    "duration_ms",
                    "error_class",
                },
            )
            self.assertEqual(metadata["schema_version"], 1)
            self.assertEqual(metadata["request_id"], artifact.request_id)
            self.assertTrue(metadata["timestamp"].endswith("Z"))
            self.assertEqual(
                datetime.fromisoformat(
                    metadata["timestamp"].replace("Z", "+00:00")
                ).tzinfo,
                timezone.utc,
            )
            self.assertEqual(metadata["provider"], "openai")
            self.assertEqual(metadata["adapter"], "codex")
            self.assertEqual(metadata["method"], "POST")
            self.assertEqual(metadata["path"], "/v1/responses")
            self.assertEqual(metadata["content_type"], "application/json")
            self.assertEqual(metadata["body_bytes"], len(body))
            self.assertEqual(
                metadata["body_sha256"], f"sha256:{hashlib.sha256(body).hexdigest()}"
            )
            self.assertEqual(metadata["response_status"], 200)
            self.assertEqual(metadata["duration_ms"], 12)
            self.assertIsNone(metadata["error_class"])
            self.assertNotIn("headers", metadata)
            self.assertNotIn("must-not-appear", artifact.metadata_path.read_text())
            self.assertEqual(stat.S_IMODE(artifact.directory.stat().st_mode), 0o700)
            self.assertEqual(stat.S_IMODE(artifact.body_path.stat().st_mode), 0o600)
            self.assertEqual(stat.S_IMODE(artifact.metadata_path.stat().st_mode), 0o600)

    def test_retention_only_deletes_marked_request_directories(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir) / "logs"
            store = RequestArtifactStore(root)
            old = store.begin_request(
                provider="anthropic",
                adapter="pi",
                method="POST",
                request_path="/v1/messages",
                content_type="application/json",
                body=b"{}",
            )
            store.complete_request(old.request_id, 200, 1)
            unmarked = old.directory.parent / "do-not-delete"
            unmarked.mkdir()
            (unmarked / "notes.txt").write_text("keep")
            old_time = time.time() - 10 * 86400
            os.utime(old.directory, (old_time, old_time))
            os.utime(unmarked, (old_time, old_time))

            removed = store.prune(retention_days=7, max_bytes=250 * 1024 * 1024)

            self.assertIn(old.request_id, removed)
            self.assertFalse(old.directory.exists())
            self.assertTrue((unmarked / "notes.txt").exists())

    def test_size_retention_removes_oldest_marked_logs_first(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir) / "logs"
            store = RequestArtifactStore(root)
            first = store.begin_request(
                "openai",
                "codex",
                "POST",
                "/v1/responses",
                "application/json",
                b"a" * 80,
            )
            store.complete_request(first.request_id, 200, 1)
            time.sleep(0.01)
            second = store.begin_request(
                "openai",
                "codex",
                "POST",
                "/v1/responses",
                "application/json",
                b"b" * 80,
            )
            store.complete_request(second.request_id, 200, 1)

            removed = store.prune(retention_days=7, max_bytes=first.size_on_disk + 20)

            self.assertIn(first.request_id, removed)
            self.assertFalse(first.directory.exists())
            self.assertTrue(second.directory.exists())

    def test_size_retention_does_not_delete_an_in_flight_request(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            store = RequestArtifactStore(Path(temp_dir) / "logs")
            active = store.begin_request(
                "openai",
                "codex",
                "POST",
                "/v1/responses",
                "application/json",
                b"a" * 80,
            )
            completed = store.begin_request(
                "openai",
                "codex",
                "POST",
                "/v1/responses",
                "application/json",
                b"b" * 80,
            )
            store.complete_request(completed.request_id, 200, 1)

            removed = store.prune(retention_days=7, max_bytes=completed.size_on_disk)

            self.assertNotIn(active.request_id, removed)
            self.assertTrue(active.directory.exists())
            store.complete_request(active.request_id, 200, 2)

    def test_list_and_show_extract_model_without_changing_body(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            store = RequestArtifactStore(Path(temp_dir) / "logs")
            body = b'{"model":"claude-test","messages":[]}'
            artifact = store.begin_request(
                "anthropic",
                "claude-code",
                "POST",
                "/v1/messages",
                "application/json",
                body,
            )
            store.complete_request(artifact.request_id, 201, 4)

            rows = store.list_requests()
            shown = store.show_request(artifact.request_id)

            self.assertEqual(rows[0]["model"], "claude-test")
            self.assertEqual(shown["body"], json.loads(body))
            self.assertEqual(artifact.body_path.read_bytes(), body)


if __name__ == "__main__":
    unittest.main()
