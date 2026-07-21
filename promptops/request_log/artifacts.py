from __future__ import annotations

import hashlib
import json
import os
import shutil
import time
import uuid
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from urllib.parse import urlsplit

from .config import _chmod_private, _write_private


MARKER = ".apastra-request-log"
BODY_FILE = "request.body"
METADATA_FILE = "metadata.json"


@dataclass(frozen=True)
class RequestArtifact:
    request_id: str
    directory: Path

    @property
    def body_path(self) -> Path:
        return self.directory / BODY_FILE

    @property
    def metadata_path(self) -> Path:
        return self.directory / METADATA_FILE

    @property
    def size_on_disk(self) -> int:
        return sum(path.stat().st_size for path in self.directory.iterdir() if path.is_file())


class RequestArtifactStore:
    def __init__(self, root: Path | str):
        self.root = Path(root).expanduser().resolve()

    def begin_request(
        self,
        provider: str,
        adapter: str,
        method: str,
        request_path: str,
        content_type: str,
        body: bytes,
    ) -> RequestArtifact:
        now = datetime.now(timezone.utc)
        request_id = uuid.uuid4().hex
        day_dir = self.root / now.strftime("%Y-%m-%d")
        directory = day_dir / f"{now.strftime('%Y%m%dT%H%M%S.%fZ')}_{request_id}"
        self.root.mkdir(parents=True, exist_ok=True, mode=0o700)
        day_dir.mkdir(parents=True, exist_ok=True, mode=0o700)
        directory.mkdir(mode=0o700)
        for private_dir in (self.root, day_dir, directory):
            _chmod_private(private_dir, directory=True)

        artifact = RequestArtifact(request_id=request_id, directory=directory)
        try:
            _write_private(directory / MARKER, b"apastra-provider-request-log-v1\n")
            _write_private(artifact.body_path, body)
            metadata = {
                "schema_version": 1,
                "request_id": request_id,
                "timestamp": now.isoformat().replace("+00:00", "Z"),
                "provider": provider,
                "adapter": adapter,
                "method": method.upper(),
                "path": urlsplit(request_path).path,
                "content_type": content_type,
                "body_bytes": len(body),
                "body_sha256": f"sha256:{hashlib.sha256(body).hexdigest()}",
                "response_status": None,
                "duration_ms": None,
                "error_class": None,
            }
            self._write_metadata(artifact.metadata_path, metadata)
        except Exception:
            shutil.rmtree(directory, ignore_errors=True)
            raise
        return artifact

    def complete_request(self, request_id: str, status: int, duration_ms: int) -> None:
        artifact = self._find(request_id)
        metadata = self._load_metadata(artifact.metadata_path)
        metadata.update({"response_status": status, "duration_ms": duration_ms, "error_class": None})
        self._write_metadata(artifact.metadata_path, metadata)

    def fail_request(self, request_id: str, error_class: str, duration_ms: int, status: int | None = None) -> None:
        artifact = self._find(request_id)
        metadata = self._load_metadata(artifact.metadata_path)
        metadata.update({"response_status": status, "duration_ms": duration_ms, "error_class": error_class})
        self._write_metadata(artifact.metadata_path, metadata)

    def list_requests(self) -> list[dict[str, Any]]:
        rows: list[dict[str, Any]] = []
        for artifact in self._iter_artifacts():
            try:
                metadata = self._load_metadata(artifact.metadata_path)
                body = artifact.body_path.read_bytes()
            except (OSError, ValueError, json.JSONDecodeError):
                continue
            row = dict(metadata)
            row["model"] = _extract_model(body)
            rows.append(row)
        return sorted(rows, key=lambda row: row.get("timestamp", ""), reverse=True)

    def show_request(self, request_id: str) -> dict[str, Any]:
        artifact = self._find(request_id)
        metadata = self._load_metadata(artifact.metadata_path)
        raw_body = artifact.body_path.read_bytes()
        try:
            body: Any = json.loads(raw_body)
        except (json.JSONDecodeError, UnicodeDecodeError):
            body = raw_body.decode("utf-8", errors="backslashreplace")
        return {"metadata": metadata, "body": body, "raw_body": raw_body}

    def prune(self, retention_days: int, max_bytes: int) -> list[str]:
        artifacts = list(self._iter_artifacts())
        removed: list[str] = []
        cutoff = time.time() - retention_days * 86400 if retention_days else None
        survivors: list[RequestArtifact] = []
        for artifact in sorted(artifacts, key=lambda item: item.directory.stat().st_mtime):
            if cutoff is not None and artifact.directory.stat().st_mtime < cutoff:
                self._remove_marked(artifact)
                removed.append(artifact.request_id)
            else:
                survivors.append(artifact)

        if max_bytes:
            total = sum(artifact.size_on_disk for artifact in survivors if artifact.directory.exists())
            for artifact in survivors:
                if total <= max_bytes:
                    break
                if not artifact.directory.exists():
                    continue
                size = artifact.size_on_disk
                self._remove_marked(artifact)
                total -= size
                removed.append(artifact.request_id)
        return removed

    def _write_metadata(self, path: Path, metadata: dict[str, Any]) -> None:
        payload = json.dumps(metadata, indent=2, sort_keys=True).encode("utf-8") + b"\n"
        temp = path.with_name(f".{path.name}.{os.getpid()}.tmp")
        _write_private(temp, payload)
        os.replace(temp, path)
        _chmod_private(path, directory=False)

    @staticmethod
    def _load_metadata(path: Path) -> dict[str, Any]:
        data = json.loads(path.read_text(encoding="utf-8"))
        if not isinstance(data, dict):
            raise ValueError("Request metadata must be an object")
        return data

    def _iter_artifacts(self):
        if not self.root.exists():
            return
        for marker in self.root.glob(f"*/*/{MARKER}"):
            directory = marker.parent
            if (directory / BODY_FILE).is_file() and (directory / METADATA_FILE).is_file():
                try:
                    request_id = self._load_metadata(directory / METADATA_FILE)["request_id"]
                except (OSError, KeyError, ValueError, json.JSONDecodeError):
                    continue
                yield RequestArtifact(str(request_id), directory)

    def _find(self, request_id: str) -> RequestArtifact:
        if not request_id or any(character not in "0123456789abcdef" for character in request_id.lower()):
            raise KeyError(f"Unknown request ID: {request_id}")
        for artifact in self._iter_artifacts():
            if artifact.request_id == request_id:
                return artifact
        raise KeyError(f"Unknown request ID: {request_id}")

    @staticmethod
    def _remove_marked(artifact: RequestArtifact) -> None:
        marker = artifact.directory / MARKER
        if not marker.is_file():
            raise RuntimeError(f"Refusing to remove unmarked directory: {artifact.directory}")
        shutil.rmtree(artifact.directory)


def _extract_model(body: bytes) -> str | None:
    try:
        data = json.loads(body)
    except (json.JSONDecodeError, UnicodeDecodeError):
        return None
    return str(data["model"]) if isinstance(data, dict) and data.get("model") is not None else None
