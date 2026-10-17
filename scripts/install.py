"""Copy only distributable Apastra assets; never prune the source or consumer."""
from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import tempfile


RUNTIME_FILES = {
    "runtime": {".py"}, "request_log": {".py"}, "resolver": {".py"},
    "runs": {".py", ".sh"}, "manifests": {".py"},
    "schemas": {".json", ".md"}, "validators": {".sh"},
    "harnesses": {".py", ".sh"}, "hooks": {".py", ".js"},
}


def digest(data):
    return hashlib.sha256(data).hexdigest()


def safe_destination(path, project):
    for candidate in (path, *path.parents):
        if candidate == project:
            break
        if candidate.is_symlink():
            raise ValueError(f"Refusing symlink install destination: {candidate}. Move it and retry.")
        if candidate != path and candidate.exists() and not candidate.is_dir():
            raise ValueError(f"Install parent is not a directory: {candidate}")


def install(source, project, links=True):
    source, project = source.resolve(), project.resolve()
    planned = {}

    def add(path, destination):
        if path.is_symlink():
            raise ValueError(f"Refusing symlink source asset: {path}")
        if path.resolve() != destination.absolute():
            planned[destination] = (path.read_bytes(), path.stat().st_mode & 0o777)

    runtime = project / ".agent/scripts/apastra"
    add(source / "promptops/__init__.py", runtime / "__init__.py")
    for directory, suffixes in RUNTIME_FILES.items():
        parent = source / "promptops" / directory
        # Python packages and validator libraries recurse. Other tool directories
        # also contain historical evidence and experimental results.
        paths = parent.rglob("*") if directory in {"runtime", "request_log", "resolver", "validators"} else parent.glob("*")
        for path in paths:
            if path.is_file() and path.suffix in suffixes and "__pycache__" not in path.parts:
                if directory != "schemas" or path.name.endswith(".schema.json") or path.suffix == ".md":
                    add(path, runtime / directory / path.relative_to(parent))
    for name in ("manifests/consumption-example.yaml", "harnesses/reference-adapter/README.md",
                 "harnesses/reference-adapter/adapter.yaml", "harnesses/reference-adapter/run.py",
                 "harnesses/promptfoo/run.py", "harnesses/promptfoo/adapter.yaml", "harnesses/promptfoo/README.md"):
        path = source / "promptops" / name
        if path.is_file():
            add(path, runtime / name)
    add(source / "bin/apastra", project / ".agent/bin/apastra")
    skills = project / ".agent/skills/apastra"
    for name in ("SKILL.md", "LICENSE", "README.md"):
        if (source / name).is_file():
            add(source / name, skills / name)
    for directory in [source / "docs", *[p for p in source.iterdir() if p.is_dir() and (p / "SKILL.md").is_file()]]:
        for path in directory.rglob("*"):
            if path.is_file() and "__pycache__" not in path.parts and path.suffix not in {".pyc", ".pyo", ".orig", ".rej"}:
                add(path, skills / path.relative_to(source))

    manifest = project / ".agent/.apastra-install.json"
    lock = project / ".agent/.apastra-install.lock"
    for path in [manifest, lock, *planned]:
        safe_destination(path, project)
    if links:
        for name in (".claude", ".agents"):
            safe_destination(project / name / "skills", project)
    manifest.parent.mkdir(parents=True, exist_ok=True)
    try:
        lock.mkdir()
    except FileExistsError:
        raise ValueError(f"Another install is active, or was interrupted: {lock}. After confirming no installer is running, remove this lock and retry.")
    try:
        previous = {}
        if manifest.exists():
            record = json.loads(manifest.read_text())
            if not isinstance(record, dict) or record.get("apastra_install") != 1 or not isinstance(record.get("files"), dict):
                raise ValueError(f"Preserving unrecognized install manifest: {manifest}. Move or back it up, then retry setup.")
            previous = record["files"]
            if not all(isinstance(key, str) and isinstance(value, str) for key, value in previous.items()):
                raise ValueError(f"Invalid install manifest: {manifest}")
        updated = dict(previous)
        for path, (data, mode) in planned.items():
            key = path.relative_to(project).as_posix()
            if path.exists():
                if not path.is_file():
                    raise ValueError(f"Install destination is not a file: {path}")
                actual = digest(path.read_bytes())
                if actual != digest(data) and actual != previous.get(key):
                    raise ValueError(f"Preserving conflicting user file: {path}. Move or back it up, then retry setup.")
            updated[key] = digest(data)
        # Individual writes are atomic. If interrupted, a retry accepts files already
        # equal to the new payload and resumes without pruning any unrelated files.
        for path, (data, mode) in planned.items():
            path.parent.mkdir(parents=True, exist_ok=True)
            if path.exists() and path.read_bytes() == data:
                continue
            atomic_write(path, data, mode)
        atomic_write(manifest, (json.dumps({"apastra_install": 1, "files": updated}, indent=2) + "\n").encode(), 0o644)
        if links:
            for name in (".claude", ".agents"):
                path = project / name / "skills/apastra"
                safe_destination(path.parent, project)
                if path.exists() or path.is_symlink():
                    if path.is_symlink() and path.resolve() == skills.resolve():
                        continue
                    print(f"Preserving existing skill path: {path}")
                    continue
                path.parent.mkdir(parents=True, exist_ok=True)
                path.symlink_to("../../.agent/skills/apastra", target_is_directory=True)
    finally:
        lock.rmdir()


def atomic_write(path, data, mode):
    descriptor, temporary = tempfile.mkstemp(prefix=".apastra-", dir=path.parent)
    try:
        with os.fdopen(descriptor, "wb") as handle:
            handle.write(data)
        os.chmod(temporary, mode)
        os.replace(temporary, path)
    finally:
        if Path(temporary).exists():
            Path(temporary).unlink()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source", type=Path)
    parser.add_argument("project", type=Path)
    parser.add_argument("--no-links", action="store_true")
    arguments = parser.parse_args()
    try:
        install(arguments.source, arguments.project, not arguments.no_links)
    except (OSError, ValueError) as error:
        parser.exit(1, f"Apastra installation failed: {error}\n")
