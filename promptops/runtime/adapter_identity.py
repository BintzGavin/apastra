"""Verify explicit adapter file pins without claiming dependency closure or authenticity."""

import hashlib
from pathlib import Path, PurePosixPath

from promptops.runtime.digest import compute_digest_from_dict
from promptops.runtime.evidence import EvidenceError


def implementation_identity(adapter_path, adapter):
    implementation = adapter.get("implementation")
    if implementation is None:
        return {"mode": "configuration_only"}
    files = implementation["files"]
    base = Path(adapter_path).resolve().parent
    for reference, expected in files.items():
        if "\\" in reference or ":" in reference or PurePosixPath(reference).is_absolute() or any(part in ("", ".", "..") for part in reference.split("/")):
            raise EvidenceError("Adapter implementation paths must be safe relative files")
        path = base
        for part in reference.split("/"):
            path = path / part
            if path.is_symlink():
                raise EvidenceError("Adapter implementation files cannot use symlinks")
        if not path.resolve().is_relative_to(base) or not path.is_file():
            raise EvidenceError("Adapter implementation file is missing or escapes its directory")
        actual = "sha256:" + hashlib.sha256(path.read_bytes()).hexdigest()
        if actual != expected:
            raise EvidenceError("Adapter implementation file content digest mismatch")
    return {"mode": "pinned_files", "digest": compute_digest_from_dict(files)}
