"""Shared CLI dispatch for Python, npm, and project-local installations."""
from __future__ import annotations

import sys


def main() -> int:
    if len(sys.argv) > 1 and sys.argv[1] == "request-log":
        from promptops.request_log.cli import main as request_log_main
        return request_log_main(sys.argv[2:])
    from promptops.runtime.cli import main as runtime_main
    result = runtime_main()
    return int(result) if result is not None else 0
